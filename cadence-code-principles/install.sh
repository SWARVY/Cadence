#!/usr/bin/env bash
# cadence-code-principles install — Claude Code 메모리 보강 (옵션)
#
# 주의: 이 스크립트는 *Claude Code 한정* 메모리 시스템 보강용.
# Codex / Copilot / Cursor / Windsurf 등은 SKILL.md 자체가 본문 + rules/ 디렉토리를
# 자동 로드하므로 별도 메모리 복제 불필요. 도구별 skill 디렉토리에 symlink 만 걸면 작동.
# (자세한 안내는 ../README.md § "도구별 skill 디렉토리에 symlink" 참조)
#
# cwd 의 Claude Code 메모리 폴더에 개인 코딩 판단 원칙 4건 복제 + MEMORY.md 인덱스 갱신
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_DIR="$SCRIPT_DIR/rules"
INDEX_FRAGMENT="$RULES_DIR/MEMORY-INDEX.md"
CWD="$(pwd)"
ENCODED="$(echo "$CWD" | sed 's|/|-|g')"
MEM_DIR="$HOME/.claude/projects/${ENCODED}/memory"
INDEX="$MEM_DIR/MEMORY.md"

FORCE=0
DRY=0
for arg in "$@"; do
  case "$arg" in
    -f|--force) FORCE=1 ;;
    -n|--dry-run) DRY=1 ;;
    -h|--help)
      cat <<EOF
cadence-code-principles install — 개인 코딩 판단 원칙 4건를 현재 프로젝트 메모리에 복제

Usage:
  $(basename "$0") [options]

Options:
  -f, --force    기존 동명 파일 무조건 덮어쓰기
  -n, --dry-run  변경 미적용, 어떤 파일이 처리될지만 출력
  -h, --help     도움말

Target: $MEM_DIR
EOF
      exit 0
      ;;
  esac
done

echo ">> cwd:       $CWD"
echo ">> mem dir:   $MEM_DIR"
echo ">> mode:      $([ $DRY -eq 1 ] && echo dry-run || echo apply) $([ $FORCE -eq 1 ] && echo force)"
echo

if [[ $DRY -eq 0 ]]; then
  mkdir -p "$MEM_DIR"
fi

copied=0
skipped=0
overwrote=0
for src in "$RULES_DIR"/feedback_*.md; do
  name="$(basename "$src")"
  dest="$MEM_DIR/$name"
  if [[ -f "$dest" ]]; then
    if [[ $FORCE -eq 1 ]]; then
      [[ $DRY -eq 0 ]] && cp "$src" "$dest"
      echo "  [overwrite] $name"
      overwrote=$((overwrote+1))
    else
      echo "  [skip]      $name (exists; use --force to overwrite)"
      skipped=$((skipped+1))
    fi
  else
    [[ $DRY -eq 0 ]] && cp "$src" "$dest"
    echo "  [copy]      $name"
    copied=$((copied+1))
  fi
done

echo
echo ">> rules: $copied copied, $overwrote overwrote, $skipped skipped"

# MEMORY.md 인덱스 갱신 — sentinel marker 안만 교체
if [[ -f "$INDEX" ]]; then
  if grep -q '<!-- cadence-code-principles start -->' "$INDEX"; then
    if [[ $DRY -eq 0 ]]; then
      awk -v frag="$INDEX_FRAGMENT" '
        BEGIN { in_block=0 }
        /<!-- cadence-code-principles start -->/ { in_block=1; while ((getline line < frag) > 0) print line; close(frag); next }
        /<!-- cadence-code-principles end -->/   { in_block=0; next }
        !in_block { print }
      ' "$INDEX" > "$INDEX.tmp" && mv "$INDEX.tmp" "$INDEX"
    fi
    echo ">> MEMORY.md: cadence-code-principles block updated in-place"
  else
    if [[ $DRY -eq 0 ]]; then
      echo "" >> "$INDEX"
      cat "$INDEX_FRAGMENT" >> "$INDEX"
    fi
    echo ">> MEMORY.md: cadence-code-principles block appended"
  fi
else
  if [[ $DRY -eq 0 ]]; then
    cp "$INDEX_FRAGMENT" "$INDEX"
  fi
  echo ">> MEMORY.md: created with cadence-code-principles block"
fi

echo
echo "Done. 다음 Claude Code 세션부터 룰이 자동 로드됩니다."
