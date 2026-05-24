---
name: 워크트리에서 절대 경로는 워크트리 경로로
description: git worktree 환경에서 Read/Write/Edit 의 절대 경로는 메인 레포가 아니라 워크트리 경로를 써야 함. 도구별 worktree 컨벤션 따름.
type: feedback
---

git worktree 환경에서 작업할 때 파일 편집의 절대 경로는 **워크트리 경로** 를 써야 한다. 메인 레포 경로(`<main-repo>/...`) 를 그대로 쓰면 사용자가 다른 브랜치로 진행 중인 *메인 워킹 트리를 침범* 한다.

**Why:** 환경 안내(`Worktree path: ...` 또는 동등) 가 있어도 절대 경로 사용 시 무심코 *레포 루트 경로* 로 향함. 메인 레포의 다른 작업 브랜치 위에 변경이 쌓이면 *patch 추출 → 워크트리 적용 → 메인 레포 git restore* 같은 회수 절차가 필요해진다.

**How to apply:**

- 워크트리 환경 활성화 신호 확인:
  - 시스템 메시지의 `Worktree path: ...` 또는 동등
  - `pwd` 가 워크트리 경로
  - `git rev-parse --show-toplevel` 이 워크트리 경로
- 모든 절대 경로는 `<worktree path>/...` 형태로 시작
- `pwd` 결과가 의심스러우면 한 번 더 확인
- 메인 레포 경로로 작업했다는 사실이 드러나면 (예: `git status` 가 *다른 브랜치*), 즉시 patch 로 추출 후 워크트리에 옮기고 메인 레포 복구

**worktree 위치 패턴 (예시):**

| 환경 | 워크트리 위치 패턴 |
| --- | --- |
| 도구가 생성한 숨김 worktree | `.<tool>/worktrees/<name>/` (cwd 내) |
| 일반 git worktree | `<repo>.worktrees/<name>` 또는 `<repo>/../<name>` 등 |
| IDE / 에이전트별 사용자 설정 | 프로젝트 또는 사용자 설정에 따름 |

워크트리 경로 *형식* 은 도구마다 다르나, **"메인 레포 경로 ≠ 작업 경로" 원칙은 동일**.
