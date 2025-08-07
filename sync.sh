#!/bin/sh

cd ~/my-ish-repo || exit 1

echo "📦 Syncing workspace..."

git add .
git commit -m "Auto-sync $(date '+%Y-%m-%d %H:%M:%S')"
git pull --rebase
git push

echo "✅ Sync complete!"
