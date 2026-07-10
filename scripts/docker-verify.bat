@echo off
REM Local Docker build & run (Sprint 9 verification)
REM Requires Docker Desktop installed
setlocal

echo === Seller Toolkit Docker Build ===

docker compose version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH.
    echo Install Docker Desktop: https://www.docker.com/products/docker-desktop/
    exit /b 1
)

if not exist .env (
    echo Copying .env.example to .env ...
    copy .env.example .env
)

echo Building and starting containers...
docker compose up -d --build

echo.
echo Waiting for services to start...
timeout /t 15 /nobreak >nul

echo.
echo === Health Check ===
curl -sf http://localhost:8080/health && echo Health OK || echo Health FAILED
curl -sf -o nul -w "Homepage: %%{http_code}\n" http://localhost:8080/
curl -sf -o nul -w "robots.txt: %%{http_code}\n" http://localhost:8080/robots.txt
curl -sf -o nul -w "sitemap.xml: %%{http_code}\n" http://localhost:8080/sitemap.xml

echo.
echo Docker running at http://localhost:8080
echo Stop: docker compose down
endlocal
