<!-- cadence-ai-behavior start -->
## cadence-ai-behavior (AI 행동 통제 룰, 도구 무관)

- [사용자 의견 = 검토 대상](feedback_collaborator_not_authority.md) — AI 의 sycophancy 통제, 반사적 동의 금지, 더 나은 안 즉시 주장
- [리뷰는 대화 오프너](feedback_review_as_dialogue.md) — 새 의견은 검토하고, 검토된 제안의 승인은 원래 요청 범위 안에서 실행
- [고추론·고비용 ↔ 저비용·실행 모델 분리](feedback_model_strategy.md) — 토큰 비용 최적화, 옵션 제시 (구체 모델 매핑은 프로젝트별)
- [원격 반영은 명시 요청 시에만](feedback_no_auto_commit_push.md) — terminal intent의 필수 단계만 수행하고 승인되지 않은 외부 작업은 차단
- [주 도구 ↔ 보조 도구 크로스 체크](feedback_crosscheck.md) — 단일 모델 편향 회피, 매트릭스 양방향
- [외부 도구 인증/세션 실패 반복 시 재시도 중단](feedback_external_tool_failure.md) — 같은 auth/session 오류 2회 반복 시 이어받기 요약 생성 후 정지
- [워크트리 절대 경로](feedback_worktree_absolute_paths.md) — AI 가 경로 헷갈려 메인 레포 침범하는 경향 통제 (도구별 worktree 컨벤션)
- [주석 간결](feedback_concise_comments.md) — AI 가 장황한 JSDoc / 절차 나열 / 자명 코드 재기술하는 경향 통제
- [무거운 해석 확정 전 가벼운 대안 제시·대기](feedback_lighter_option_before_heavy_commit.md) — 모호 지시/가벼움↔무거움 갈림길에서 무거운 쪽 빌드아웃 전 멈추고 선택 대기 (옵션 제시만으론 부족)
<!-- cadence-ai-behavior end -->
