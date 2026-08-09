<!-- cadence-ai-behavior start -->
## cadence-ai-behavior (AI 행동 통제 룰, 도구 무관)

- [사용자 의견 = 검토 대상](feedback_collaborator_not_authority.md) — AI 의 sycophancy 통제, 반사적 동의 금지, 더 나은 안 즉시 주장
- [리뷰는 대화 오프너](feedback_review_as_dialogue.md) — 완곡한 새 제안은 의견으로 분류하고, 현재 이유·적용 전제·평가·추천을 공유한 뒤 명시적 실행 요청만 편집으로 전환
- [고추론·고비용 ↔ 저비용·실행 모델 분리](feedback_model_strategy.md) — 토큰 비용 최적화, 옵션 제시 (구체 모델 매핑은 프로젝트별)
- [원격 반영은 명시 요청 시에만](feedback_no_auto_commit_push.md) — terminal action preflight와 실행 후 postcondition을 거쳐 승인된 단계만 보고하고, 완료된 변경 사이클의 권한 승계를 차단
- [주 도구 ↔ 보조 도구 크로스 체크](feedback_crosscheck.md) — plan task와 review slice를 분리하고, 낮은 위험은 생략하며 load-bearing finding과 누적 위험에서만 독립 리뷰 경로를 확대
- [외부 도구 인증/세션 실패 반복 시 재시도 중단](feedback_external_tool_failure.md) — 같은 auth/session 오류 2회 반복 시 이어받기 요약 생성 후 정지
- [워크트리 절대 경로](feedback_worktree_absolute_paths.md) — AI 가 경로 헷갈려 메인 레포 침범하는 경향 통제 (도구별 worktree 컨벤션)
- [주석 간결](feedback_concise_comments.md) — AI 가 장황한 JSDoc / 절차 나열 / 자명 코드 재기술하는 경향 통제
- [무거운 해석 확정 전 가벼운 대안 제시·대기](feedback_lighter_option_before_heavy_commit.md) — 모호 지시/가벼움↔무거움 갈림길에서 무거운 쪽 빌드아웃 전 멈추고 선택 대기 (옵션 제시만으론 부족)
<!-- cadence-ai-behavior end -->
