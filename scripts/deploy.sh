#!/usr/bin/env bash
# Wrapper — runs project-root deploy.sh
# Usage: bash scripts/deploy.sh
exec "$(cd "$(dirname "$0")/.." && pwd)/deploy.sh" "$@"
