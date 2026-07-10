# Seller Toolkit

> Global Seller Toolkit — Free tools for eCommerce sellers.

**Version:** V1.0

## Tech Stack

- **Backend:** FastAPI + Jinja2 + SQLAlchemy + Alembic
- **Frontend:** Bootstrap 5 + HTML5 + JavaScript
- **Database:** MySQL 8
- **AI:** DeepSeek API
- **Deployment:** Docker + Docker Compose + Nginx

## Development Workflow

**日常开发**使用 FastAPI + Laragon + MySQL 8 直接运行，**不使用 Docker**。

**仅在以下情况使用 Docker：** Sprint 验收、Release 发布、生产部署。

### Prerequisites

- Python 3.13（Laragon）
- MySQL 8（Laragon）
- Git

### Local Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
copy .env.example .env       # Windows
# cp .env.example .env       # Linux

# Create database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS sisuu_tools CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8888
```

Visit: http://127.0.0.1:8888

> Laragon 域名 `http://sisuu.com.test` 通过 `index.html` 跳转到 8888。

---

## Docker Deployment (Local Verification)

需要安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。

```bash
# Windows
scripts\docker-verify.bat

# Linux / Mac
docker compose up -d --build
curl http://localhost:8080/health
```

访问: http://localhost:8080

容器启动时自动执行 `alembic upgrade head`（见 `scripts/docker-entrypoint.sh`）。

---

## Production Deployment (Oracle Cloud / Ubuntu 24.04)

### 1. Server Setup

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Clone project
sudo mkdir -p /opt/seller-toolkit
sudo chown $USER:$USER /opt/seller-toolkit
git clone <repo-url> /opt/seller-toolkit
cd /opt/seller-toolkit

# Configure environment
cp .env.example .env
nano .env   # Set SECRET_KEY, DEEPSEEK_API_KEY, ADMIN_PASSWORD, MYSQL_ROOT_PASSWORD
```

### 2. SSL Certificate (Let's Encrypt)

```bash
sudo bash scripts/setup-ssl.sh your@email.com
```

### 3. Deploy

```bash
sudo bash scripts/deploy.sh
```

或手动：

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

访问: https://sisuu.com

### 4. Post-Launch Checklist

- [ ] https://sisuu.com 首页正常
- [ ] https://sisuu.com/robots.txt
- [ ] https://sisuu.com/sitemap.xml
- [ ] https://sisuu.com/health
- [ ] 6 个核心工具可运行
- [ ] Google Search Console 提交 Sitemap
- [ ] Bing Webmaster 提交 Sitemap

### 5. Database Backup

```bash
# Manual backup
bash scripts/backup-db.sh

# Cron (daily 3am, keep 7 days)
0 3 * * * /opt/seller-toolkit/scripts/backup-db.sh
```

### 6. Update Workflow

```bash
cd /opt/seller-toolkit
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

---

## Project Structure

```
app/
├── main.py           # FastAPI entry
├── config.py         # Settings from .env
├── routes/           # Route handlers
├── services/         # Business logic
├── templates/        # Jinja2 templates
└── static/           # CSS, JS, images, vendor
nginx/
├── nginx.conf        # Local Docker (HTTP :8080)
└── nginx.prod.conf   # Production (HTTPS)
scripts/
├── docker-entrypoint.sh
├── deploy.sh
├── setup-ssl.sh
└── backup-db.sh
```

## Documentation

All development standards are in the `docs/` directory.

## License

Proprietary — All rights reserved.
