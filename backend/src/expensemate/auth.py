from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta
from hmac import compare_digest

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from expensemate.models import AuthLoginRequest, AuthRegisterRequest, User, UserSession
from expensemate.settings import settings


PBKDF2_ITERATIONS = 200_000


class AuthError(ValueError):
    pass


def normalize_email(email: str) -> str:
    return email.strip().lower()


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    derived = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), PBKDF2_ITERATIONS)
    return f'pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${derived.hex()}'


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected = password_hash.split('$', 3)
    except ValueError:
        return False
    if algorithm != 'pbkdf2_sha256':
        return False
    derived = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        int(iterations),
    ).hex()
    return compare_digest(derived, expected)


def create_session_token() -> str:
    return secrets.token_urlsafe(32)


def hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def build_user_read(user: User):
    from expensemate.models import AuthUserRead

    return AuthUserRead(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    normalized = normalize_email(email)
    result = await session.exec(select(User).where(User.email == normalized))
    return result.first()


async def register_user(session: AsyncSession, payload: AuthRegisterRequest) -> User:
    existing = await get_user_by_email(session, payload.email)
    if existing is not None:
        raise AuthError('An account with this email already exists.')

    user = User(
        name=payload.name.strip(),
        email=normalize_email(payload.email),
        password_hash=hash_password(payload.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_session(session: AsyncSession, user: User) -> str:
    token = create_session_token()
    user_session = UserSession(
        user_id=user.id,
        token_hash=hash_session_token(token),
        expires_at=datetime.utcnow() + timedelta(days=settings.session_max_age_days),
    )
    session.add(user_session)
    await session.commit()
    return token


async def authenticate_user(session: AsyncSession, payload: AuthLoginRequest) -> tuple[User, str]:
    user = await get_user_by_email(session, payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AuthError('Invalid email or password.')
    token = await create_session(session, user)
    return user, token


async def get_user_by_session_token(session: AsyncSession, token: str | None) -> User | None:
    if not token:
        return None

    now = datetime.utcnow()
    token_hash = hash_session_token(token)
    session_result = await session.exec(
        select(UserSession).where(UserSession.token_hash == token_hash).where(UserSession.expires_at > now)
    )
    active_session = session_result.first()
    if active_session is None:
        stale_result = await session.exec(select(UserSession).where(UserSession.token_hash == token_hash))
        stale = stale_result.first()
        if stale is not None:
            await session.delete(stale)
            await session.commit()
        return None

    return await session.get(User, active_session.user_id)


async def revoke_session_token(session: AsyncSession, token: str | None) -> None:
    if not token:
        return
    token_hash = hash_session_token(token)
    result = await session.exec(select(UserSession).where(UserSession.token_hash == token_hash))
    user_session = result.first()
    if user_session is None:
        return
    await session.delete(user_session)
    await session.commit()
