#!/bin/bash
# CloudPilot lab bootstrap. Runs ONCE at first boot, as root.
# Output: /var/log/cloud-init-output.log
set -euo pipefail

REGION="us-east-1"
PARAM_PATH="/cloudpilot/lab"
APP_DIR="/opt/cloudpilot"
COMPOSE_VERSION="v2.29.7"

echo "==> 1. Install Docker + Compose plugin"
dnf install -y docker
systemctl enable --now docker
mkdir -p /usr/local/lib/docker/cli-plugins
curl -fsSL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-x86_64" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

echo "==> 2. Read secrets from SSM (via the instance's IAM role)"
get_param() {
  # Retry: the IAM role's credentials can take a few seconds to appear after boot
  for _ in $(seq 1 10); do
    if aws ssm get-parameter --region "$REGION" --name "$PARAM_PATH/$1" \
         --with-decryption --query Parameter.Value --output text; then
      return 0
    fi
    sleep 5
  done
  echo "ERROR: could not read $PARAM_PATH/$1" >&2
  return 1
}
DB_PASSWORD="$(get_param POSTGRES_PASSWORD)"
JWT_SECRET="$(get_param SECRET_KEY)"

echo "==> 3. Write config (.env readable by root only)"
mkdir -p "$APP_DIR"
umask 077
cat > "$APP_DIR/.env" <<EOF
ENV=prod
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=cloudpilot
POSTGRES_USER=cloudpilot
POSTGRES_PASSWORD=${DB_PASSWORD}
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=${JWT_SECRET}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
umask 022

cat > "$APP_DIR/docker-compose.yml" <<'EOF'
services:
  postgres:
    image: postgres:15-alpine
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
      interval: 5s
      retries: 12
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  api:
    image: ghcr.io/rxmbtw/cloudpilot-api:main
    env_file: .env
    command: sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    ports:
      - "80:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

volumes:
  pgdata:
EOF

echo "==> 4. Start the app"
cd "$APP_DIR"
docker compose up -d
echo "==> CloudPilot bootstrap complete"
