# Local setup

Python 3.10+ is required. This adapter targets Laya 0.3.5's direct SDK; newer versions require compatibility testing. A separate virtual environment is recommended. After choosing a runtime location:

```sh
python3 -m venv /absolute/path/to/laya-venv
/absolute/path/to/laya-venv/bin/python -m pip install -r /absolute/path/to/installed/skill/requirements.txt
```

Choose a supported checkpoint using [upstream Laya](https://github.com/NandhaKishorM/laya). Prepare weights separately with the user's agreement; this adapter only loads a local directory and forces Hugging Face offline mode. Korean trials need a multilingual checkpoint. The SDK's device fallback can use CPU; actual inference reports the device. Its tokenizer compatibility helper may normalize tokenizer metadata in the supplied model directory.

Create a private JSON config outside the distributed skill:

```json
{
  "enabled": true,
  "mode": "shadow",
  "python": "/absolute/path/to/laya-venv/bin/python",
  "model_path": "/absolute/path/to/multilingual-checkpoint",
  "device": "cpu",
  "languages": ["ko", "en"],
  "timeout_seconds": 60,
  "min_confidence": 0.8
}
```

`languages` is the operator's declaration for the selected checkpoint, not automatic language detection. Paths must be absolute, with no machine-specific default. `enabled: false` or no config disables invocation. Only `shadow` mode is implemented in this initial release. Do not point to a remote model ID. Threshold 0.8 is a smoke-test starting value, not validated for Cadence quality.

```sh
python3 /absolute/path/to/skill/scripts/adapter.py doctor --config /absolute/path/to/config.json
python3 /absolute/path/to/skill/scripts/adapter.py smoke --config /absolute/path/to/config.json
```

Doctor checks Python, pinned package version, PyTorch import, and local model files. Smoke actually loads the model and classifies optional references, returning device and elapsed time. Neither proves workflow improvement. Evaluate required-reference recall, false exclusions, abstentions, and end-to-end time including cold load and main-agent review before considering a future live mode.

The config contains local paths and is not part of the public package. Store it in your normal private configuration directory; supply `--config` or `CADENCE_LAYA_CONFIG`. No global installation or project bootstrap is modified automatically.
