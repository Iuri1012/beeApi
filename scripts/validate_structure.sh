#!/bin/bash

echo "🐝 BeeAPI Structure Validation"
echo ""

# Check critical files exist
files_to_check=(
    "README.md"
    "LICENSE"
    ".gitignore"
    "docker-compose.yml"
    "firmware/simulator.py"
    "firmware/pyproject.toml"
    "backend/main.py"
    "backend/Dockerfile"
    "backend/pyproject.toml"
    "telemetry/consumer.py"
    "telemetry/Dockerfile"
    "telemetry/pyproject.toml"
    "timeseries/init.sql"
    "web/package.json"
    "web/Dockerfile"
    "web/src/App.js"
    "scripts/run_local.sh"
    ".github/workflows/ci.yml"
    ".github/ISSUE_TEMPLATE/bug_report.md"
    ".github/ISSUE_TEMPLATE/feature_request.md"
    ".github/pull_request_template.md"
    "docs/README.md"
    "docs/API.md"
)

missing=0
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (missing)"
        missing=$((missing + 1))
    fi
done

echo ""
if [ $missing -eq 0 ]; then
    echo "✅ All required files present!"
    exit 0
else
    echo "❌ $missing file(s) missing"
    exit 1
fi
