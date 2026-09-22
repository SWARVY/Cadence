---
name: cadence-laya
description: Connect or diagnose a local Laya runtime for Cadence reference-selection trials. Use when setting up this optional adapter or evaluating reference recommendations with an explicitly configured runtime.
---

# Cadence Laya adapter

This optional skill, distributed in the Cadence repository, implements `reference-selection` contract version 1 in shadow mode. It recommends references; the main agent still performs normal reference selection and keeps mandatory rules. The package does not implement review triage or establish performance benefits.

## Setup and invocation

Read [setup](references/setup.md) when configuring a runtime or diagnosing a missing model. Installing this skill does not install Python dependencies, download weights, or activate it. Use the official `skills` CLI to install the skill; runtime preparation is a separate explicit setup step.

For a configured trial, read [the protocol](references/protocol.md). Resolve `scripts/adapter.py` relative to this installed skill directory, never a guessed repository path. Run with any Python 3.10+ launcher:

```text
python3 <skill-directory>/scripts/adapter.py doctor --config <local-config>
python3 <skill-directory>/scripts/adapter.py predict --config <local-config> --input <request-json>
```

The config can alternatively be supplied through `CADENCE_LAYA_CONFIG`. Absence or disabled config means use baseline Cadence immediately. Do not scan the user's filesystem for runtimes on every task. Explicit setup may locate an existing user-specified installation.

Use only for a bounded reference-selection trial with permitted input. Direct path checks and small obvious decisions stay on the main path. Recommendations never grant approval, suppress mandatory rules, prove verification, or create a new user gate. Validate returned IDs against the request; load and inspect references before applying their guidance.

`doctor` checks packages and local model files, not inference. `smoke` loads the actual model and runs a Korean synthetic reference-selection request. Successful inference proves connectivity only. Keep recommendations in shadow mode until task-specific quality and total cost have been evaluated.

Errors yield `status: fallback`, a reason code, and `fallback: baseline`. Continue baseline work; report failed explicit diagnostics as failed. Do not silently install dependencies, download models, change the configured interpreter, or retry indefinitely.

For known test coverage and limitations, read [verification](references/verification.md). Repository maintainers can run `python3 -m unittest discover -s tests -p 'test_laya_adapter.py' -v` from the Cadence repository root.
