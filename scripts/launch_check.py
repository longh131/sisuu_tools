#!/usr/bin/env python3
"""Pre-launch environment and route checks for Seller Toolkit V1.0."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

ISSUES: list[str] = []
WARNINGS: list[str] = []
PASSED: list[str] = []


def check(name: str, ok: bool, msg: str = "", warn: bool = False):
    if ok:
        PASSED.append(name)
    elif warn:
        WARNINGS.append(f"{name}: {msg}")
    else:
        ISSUES.append(f"{name}: {msg}")


def main() -> int:
    print("=== Seller Toolkit Launch Check ===\n")

    # .env
    env_path = ROOT / ".env"
    check(".env exists", env_path.exists(), "Copy from .env.example")

    if env_path.exists():
        from dotenv import dotenv_values
        env = dotenv_values(env_path)

        debug = str(env.get("DEBUG", "false")).lower()
        check("DEBUG=false", debug in ("false", "0", ""), f"DEBUG={debug}", warn=False)

        secret = env.get("SECRET_KEY", "")
        check("SECRET_KEY set", bool(secret) and secret != "change-me-to-a-random-secret-key",
              "Use a random 32+ char secret", warn=True)

        admin_pw = env.get("ADMIN_PASSWORD", "")
        check("ADMIN_PASSWORD changed", admin_pw not in ("", "admin123"),
              "Change default admin password", warn=True)

        check("DEEPSEEK_API_KEY", bool(env.get("DEEPSEEK_API_KEY")),
              "AI tools need API key", warn=True)

        ga = env.get("GA_MEASUREMENT_ID", "")
        check("GA_MEASUREMENT_ID", bool(ga), "Recommended for launch analytics", warn=True)

    # App import
    try:
        from app.config import get_settings
        from app.data.seed_tools import SEED_TOOLS
        from app.data.seed_blog import SEED_BLOG_POSTS
        from app.utils.seo import generate_sitemap_xml, generate_robots_txt
        settings = get_settings()
        check("App imports", True)
        check("Tools count >= 45", len(SEED_TOOLS) >= 45, f"got {len(SEED_TOOLS)}")
        check("Blog count >= 11", len(SEED_BLOG_POSTS) >= 11, f"got {len(SEED_BLOG_POSTS)}")
        sitemap = generate_sitemap_xml()
        check("Sitemap includes /pricing", "/pricing" in sitemap)
        check("Sitemap includes tools", "/tools/amazon-fee-calculator" in sitemap)
        check("Robots disallows /admin", "Disallow: /admin/" in generate_robots_txt())
        check("Payment provider stub", settings.payment_provider == "stub")
    except Exception as exc:
        check("App imports", False, str(exc))

    # Payment module
    try:
        from app.payment import get_payment_provider
        provider = get_payment_provider()
        check("Payment stub available", provider.name == "stub" and not provider.is_available())
    except Exception as exc:
        check("Payment module", False, str(exc))

    # Docker files
    check("Dockerfile", (ROOT / "Dockerfile").exists())
    check("docker-compose.yml", (ROOT / "docker-compose.yml").exists())
    check("nginx.prod.conf", (ROOT / "nginx" / "nginx.prod.conf").exists())

    # Static assets
    check("og-default.png", (ROOT / "app" / "static" / "images" / "og-default.png").exists(), warn=True)

    print(f"PASSED ({len(PASSED)}):")
    for p in PASSED:
        print(f"  [OK] {p}")

    if WARNINGS:
        print(f"\nWARNINGS ({len(WARNINGS)}):")
        for w in WARNINGS:
            print(f"  [WARN] {w}")

    if ISSUES:
        print(f"\nISSUES ({len(ISSUES)}):")
        for i in ISSUES:
            print(f"  [FAIL] {i}")
        print("\nFix issues before production launch.")
        return 1

    print("\nAll critical checks passed.")
    if WARNINGS:
        print("Review warnings before go-live.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
