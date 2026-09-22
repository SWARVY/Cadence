import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/cadence-laya/scripts/adapter.py"
spec = importlib.util.spec_from_file_location("adapter", SCRIPT)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.config = {"languages": ["ko", "en"]}
        self.request = adapter.smoke_request()

    def test_missing_config_returns_machine_readable_baseline(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "doctor", "--config", "/missing/config.json"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["fallback"], "baseline")

    def test_disabled_config_does_not_require_runtime(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "config.json"
            file.write_text('{"enabled": false}')
            with self.assertRaisesRegex(adapter.Invalid, "disabled"):
                adapter.config_at(file)

    def test_duplicate_ids_rejected(self):
        self.request["references"][1]["id"] = "approval"
        with self.assertRaisesRegex(adapter.Invalid, "invalid_reference_id"):
            adapter.validate_request(self.request, self.config)

    def test_unsupported_task_language_and_version(self):
        for field, value in (("task", "review-triage"), ("language", "fr"), ("contract_version", True)):
            with self.subTest(field=field), self.assertRaises(adapter.Invalid):
                adapter.validate_request(dict(self.request, **{field: value}), self.config)

    def test_excessive_input_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "input.json"
            file.write_text(' ' * (adapter.MAX_BYTES + 1))
            with self.assertRaisesRegex(adapter.Invalid, "input_too_large"):
                adapter.read_json(file)

    def test_invalid_or_low_confidence(self):
        answer = {"choice": "relevant", "confidence": 0.4,
                  "probabilities": {"relevant": 0.6, "unrelated": 0.2, "insufficient": 0.2}}
        self.assertEqual(adapter.interpret({"id": "x"}, answer, 0.8)["decision"], "abstain")
        for field, value in (("choice", "execute"), ("confidence", float("nan")), ("probabilities", {})):
            with self.subTest(field=field), self.assertRaises(adapter.Invalid):
                adapter.interpret({"id": "x"}, dict(answer, **{field: value}), 0.8)

    def test_mandatory_preserved_even_when_optional_excluded(self):
        class Agent:
            device = "cpu"
            def predict(self, state, questions):
                return {"answers": {"relevance": {"choice": "unrelated", "confidence": 0.99,
                        "probabilities": {"relevant": 0.005, "unrelated": 0.99, "insufficient": 0.005}}}}
        with patch.object(adapter, "check_budget"):
            result = adapter.predict(Agent(), self.request, 0.8)
        self.assertEqual(result["selected_ids"], ["approval"])
        self.assertEqual(len(result["items"]), 3)
        self.assertEqual(result["mode"], "shadow")
        self.assertEqual(result["fallback"], "baseline")

    def test_timeout_has_no_partial_advice(self):
        with patch.object(adapter.subprocess, "run", side_effect=subprocess.TimeoutExpired("worker", 1)):
            result = adapter.launch({"python": sys.executable, "timeout_seconds": 1}, "smoke", self.request)
        self.assertEqual(result, adapter.fallback("runtime_timeout"))

    def test_context_overflow_rejected_before_prediction(self):
        class Tokenizer:
            mask_token = "[MASK]"
            def __call__(self, value, **kwargs):
                return {"input_ids": value.split()}
        agent = types.SimpleNamespace(tok=Tokenizer(), cfg={"max_len": 50, "head_max_len": 256})
        common = types.ModuleType("laya.common")
        common.render_options = lambda q: list(q["crit"].keys())
        common.serialize_state = lambda state: state
        with patch.dict(sys.modules, {"laya.common": common}):
            adapter.check_budget(agent, "short input")
            with self.assertRaisesRegex(adapter.Invalid, "context_budget_exceeded"):
                adapter.check_budget(agent, "word " * 100)

    def test_worker_output_corruption_is_fallback(self):
        proc = subprocess.CompletedProcess([], 0, stdout="warning\n{}", stderr="")
        with patch.object(adapter.subprocess, "run", return_value=proc):
            result = adapter.launch({"python": sys.executable, "timeout_seconds": 1}, "doctor")
        self.assertEqual(result["reason_code"], "runtime_failed")

    def test_incomplete_or_wrong_command_output_is_fallback(self):
        for command, output in (("predict", {"status": "advisory"}),
                                ("predict", {"status": "ready"}),
                                ("doctor", {"status": "advisory"}),
                                ("doctor", {"status": "fallback"})):
            with self.subTest(command=command, output=output):
                proc = subprocess.CompletedProcess([], 0, stdout=json.dumps(output), stderr="")
                with patch.object(adapter.subprocess, "run", return_value=proc):
                    result = adapter.launch({"python": sys.executable, "timeout_seconds": 1}, command, self.request)
                self.assertEqual(result, adapter.fallback("runtime_failed"))

    def test_output_reference_invariants(self):
        output = {"contract_version": 1, "task": "reference-selection", "status": "advisory",
                  "mode": "shadow", "fallback": "baseline", "selected_ids": ["approval"],
                  "items": [{"id": ref["id"], "decision": "include" if ref["required"] else "abstain",
                             "reason_code": "required" if ref["required"] else "uncertain"}
                            for ref in self.request["references"]]}
        variants = [output]
        for mutate in (lambda v: v.update(contract_version=True),
                       lambda v: v.update(mode="live"),
                       lambda v: v.update(selected_ids=[]),
                       lambda v: v["items"].pop(),
                       lambda v: v["items"][1].update(id="unknown"),
                       lambda v: v["items"][1].update(id="approval"),
                       lambda v: v["items"][0].update(decision="exclude"),
                       lambda v: v["items"][1].update(reason_code="")):
            variant = json.loads(json.dumps(output))
            mutate(variant)
            variants.append(variant)
        for i, variant in enumerate(variants):
            with self.subTest(i=i):
                proc = subprocess.CompletedProcess([], 0, stdout=json.dumps(variant), stderr="")
                with patch.object(adapter.subprocess, "run", return_value=proc):
                    result = adapter.launch({"python": sys.executable, "timeout_seconds": 1}, "predict", self.request)
                self.assertEqual(result["status"], "advisory" if i == 0 else "fallback")

    def test_shell_not_used_and_offline_environment(self):
        proc = subprocess.CompletedProcess([], 0, stdout='{"status":"ready"}', stderr="")
        with patch.object(adapter.subprocess, "run", return_value=proc) as run:
            adapter.launch({"python": "/some path/python", "timeout_seconds": 3}, "doctor")
        self.assertEqual(run.call_args.args[0][0], "/some path/python")
        self.assertNotIn("shell", run.call_args.kwargs)
        self.assertEqual(run.call_args.kwargs["env"]["HF_HUB_OFFLINE"], "1")


if __name__ == "__main__":
    unittest.main()
