#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/6] Checking required files..."
for path in docker-compose.yml backend/pyproject.toml backend/src/expensemate/main.py frontend/app.js caddy/Caddyfile README.md LICENSE; do
  [[ -f "$path" ]] || { echo "Missing: $path"; exit 1; }
done

echo "[2/6] Checking backend syntax..."
python3 -m py_compile backend/src/expensemate/*.py

echo "[3/6] Checking frontend syntax..."
node --check frontend/app.js

echo "[4/6] Checking Docker availability..."
if command -v docker >/dev/null 2>&1; then
  docker --version
  if docker compose version >/dev/null 2>&1; then
    docker compose version
  else
    echo "docker compose plugin not found"
  fi
else
  echo "docker not installed on this machine"
fi

echo "[5/6] Running backend tests if dependencies are installed..."
if python3 - <<'PY'
import importlib.util, sys
mods = ['sqlalchemy', 'fastapi', 'sqlmodel', 'pytest', 'aiosqlite']
missing = [m for m in mods if importlib.util.find_spec(m) is None]
print(','.join(missing))
raise SystemExit(1 if missing else 0)
PY
then
  (cd backend && pytest -q)
else
  echo "Skipping backend tests because Python dependencies are missing."
  echo "Install them with: cd backend && pip install -e .[test]"
fi

echo "[6/6] Reminder: update LICENSE author name and README repo URL before final submission."
echo "Done."
