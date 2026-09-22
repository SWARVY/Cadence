# Reference-selection v1

Input is a JSON object with exactly these fields:

```json
{
  "contract_version": 1,
  "task": "reference-selection",
  "language": "ko",
  "summary": "저장 후 새 세션에서도 값이 유지되는지 확인한다.",
  "references": [
    {"id": "verification", "description": "실제 저장과 재조회 검증", "required": true},
    {"id": "review", "description": "리뷰 지적과 변경 범위 판단", "required": false}
  ]
}
```

IDs are unique opaque strings; they are not paths to open or commands to run. Up to 16 references, 32 KiB request file, bounded string fields. Each optional reference is evaluated separately against the summary, avoiding a long choice label list. Mandatory references bypass the model and remain selected. Unsupported tasks, languages, malformed JSON, duplicate IDs and excessive inputs return fallback. Token budget checks reject any state that the pinned SDK would truncate.

Success returns `status: advisory`, `mode: shadow`, contract version, task, `provider: laya`, `items`, `selected_ids`, `fallback: baseline`, and timing. Each item contains its original ID, `decision: include | exclude | abstain`, probability distribution, confidence, and a machine-readable `reason_code`. Mandatory items have no model scores. Uncertain optional items abstain and remain on the baseline path. Laya does not generate a rationale; reason codes describe adapter processing only.

The threshold is a trial parameter, not a calibrated accuracy claim. `selected_ids` is a shadow recommendation, never authority to omit required references. Confidence is checked after inference; missing/non-finite scores or invalid choices invalidate the result. Runtime failures return no partial recommendations.

The launcher bounds the runtime subprocess with the configured timeout and captures its stdout. The final stdout is one JSON object. Fallback returns exit code 2; successful doctor/advisory returns 0. Inputs are passed over stdin to the worker, not shell commands. Logs and config paths are not included in shared output. No arbitrary task/question execution is exposed.
