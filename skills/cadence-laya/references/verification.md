# Verification

Initial local verification, 2026-09-23. No workflow speedup or live-mode approval is claimed.

- Unit checks: 13 tests passed covering missing/disabled configuration, duplicate IDs, unsupported task/language/version, oversized input, invalid/low confidence, mandatory reference preservation, context overflow, timeout, malformed worker output, command-specific output contracts, and offline shell-free dispatch. The output-contract regression tests failed before adding boundary validation and passed afterward.
- Cadence integration: official skills CLI 1.5.26 with Node 22 found all five skills, including cadence-laya, using `skills add . --list` from the Cadence root. This was discovery only, not installation. An offline attempt lacked the npm cache; the subsequent network-enabled check passed.
- Skill format: official skill-creator validator passed using an existing Python environment with YAML support. The system Python initially lacked YAML; no dependency was installed into it.
- Doctor: actual Laya 0.3.5 and PyTorch 2.14.0 imported, local multilingual checkpoint files present.
- Actual Korean smoke: CPU, 27.805 seconds including runtime startup and model load, 170 input tokens reported by the SDK. Required reference preserved. Both optional references abstained at trial threshold 0.8 (confidence 0.2408 and 0.3671).

After relocation into Cadence, all 11 unit tests, skill format validation, and actual runtime doctor passed again. The pre-publication Korean smoke also passed in 31.155 seconds on CPU with the same decisions and 170 input tokens. The smoke proves JSON-to-SDK-to-result connectivity and conservative abstention. It does not establish reference-selection usefulness: this sample produced no actionable optional recommendation. Do not lower the threshold merely to make the smoke produce recommendations. Evaluate task fit, language, question design and total cost on separate cases first.

Not run: clean-machine dependency/model installation, GPU/MPS inference, independent agent workflow evaluation, comparative quality/cost benchmark, remote installation from a published repository. No model weights or private runtime paths are distributed.

Independent Luna Max review identified missing validation of syntactically valid but incomplete worker output. After the fix, the reviewer confirmed the finding resolved and independently reran all 13 tests. The final real Korean CPU smoke with boundary validation passed in 36.854 seconds, with the same mandatory inclusion and optional abstentions. This timing is a single run, not a benchmark.
