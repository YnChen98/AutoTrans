#!/usr/bin/env bash
set -euo pipefail

echo "== AutoTrans pre-Codex checkpoint =="

echo
echo "Repo root:"
git rev-parse --show-toplevel

echo
echo "Branch:"
git branch --show-current

echo
echo "HEAD:"
git rev-parse HEAD

echo
echo "Status:"
git status --short

echo
echo "Diff stat:"
git diff --stat || true

echo
echo "Staged diff stat:"
git diff --cached --stat || true

echo
UNTRACKED="$(git ls-files --others --exclude-standard)"
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$UNTRACKED" ]; then
  echo "WARNING: working tree is not clean."
  echo "Commit, stash, or intentionally keep these changes before giving Codex an edit task."
else
  echo "OK: working tree is clean."
fi
