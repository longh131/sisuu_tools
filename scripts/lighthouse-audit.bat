@echo off
REM Lighthouse audit — Sprint 8 (mobile + desktop)
REM Usage: scripts\lighthouse-audit.bat [url]

setlocal
set URL=%1
if "%URL%"=="" set URL=http://127.0.0.1:8888/

echo === Mobile (default) ===
call npx --yes lighthouse %URL% --only-categories=performance,seo,accessibility,best-practices --chrome-flags="--headless" --output=json --output-path=./lighthouse-mobile.json --quiet

echo === Desktop ===
call npx --yes lighthouse %URL% --preset=desktop --only-categories=performance,seo,accessibility,best-practices --chrome-flags="--headless" --output=json --output-path=./lighthouse-desktop.json --quiet

echo Reports: lighthouse-mobile.json, lighthouse-desktop.json
endlocal
