# Tests

Ideally, all core classes and methods should have fast, quality tests associated with
them.

## Layout

Tests live in a `tests` folder within the subpackage containing the module under test,
in a file named `test_[module_name].py`:

```
- shared
    - vault
        - __init__.py
        - client.py
        - tests
            - __init__.py
            - test_vault_client.py
```

Tests are written with the standard library `unittest` package and run under pytest.
Refer to [shared/vault/tests/test_vault_client.py](../shared/vault/tests/test_vault_client.py)
for an example.

## Running

From the repo root:

```bash
pytest
```

Configuration lives in the root `pyproject.toml` (`[tool.pytest.ini_options]`), which
adds the repo root to the import path and sets the test paths.

- The ML-free unit suites under `shared/` run anywhere.
- The `ai_service/ai_pipeline` tests drive a real local Ollama server and the
  sentence-transformers model. They are gated behind `RUN_OLLAMA_TESTS=1` so a normal
  run skips them. Run them with `RUN_OLLAMA_TESTS=1 pytest ai_service` once a model
  server is available.
- CI runs the ML-free suites (`shared/account_manager/tests`, `shared/vault/tests`) on
  every push and pull request to `main`.

See [ROADMAP.md](ROADMAP.md) for current coverage gaps.
