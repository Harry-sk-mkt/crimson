#!/usr/bin/env bash
# safe-clasp-push.sh — leaves/scripts/safe-clasp-push.sh와 같은 worktree 안전장치.
# reimburse/는 루트 저장소 안의 폴더라 git 루트가 아니라 이 스크립트의 상위 폴더에서 push한다.
set -euo pipefail

cd "$(dirname "$0")/.."
worktree_list="$(git worktree list)"
worktree_count="$(printf '%s\n' "$worktree_list" | wc -l)"
echo "=== git worktree list ==="
printf '%s\n' "$worktree_list"
echo "대상 scriptId: $(grep -o '"scriptId"[^,]*' .clasp.json)"

if [ "$worktree_count" -ge 2 ]; then
  read -r -p "worktree가 ${worktree_count}개입니다. 그래도 push할까요? (y/N) " confirm
  case "$confirm" in y|Y|yes|YES) ;; *) echo "취소"; exit 1 ;; esac
fi

node tests/parse.test.js
clasp push --force "$@"
