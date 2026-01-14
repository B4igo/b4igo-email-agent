# b4igo-email-agent


## Setup

Install the requirements (it's recommended to create a pyenv or conda environment first).
 ```bash
   pip install -r requirements.txt
   ```
Install the git hooks:
   ```bash
   pre-commit install
   ```

## Using commit hooks

Once installed, the hooks will run automatically on `git commit`. If any hook fails, the commit will be blocked.

### Manual execution

Run hooks on all files:
```bash
pre-commit run --all-files
```

Run hooks on staged files only:
```bash
pre-commit run
```

Run a specific hook:
```bash
pre-commit run black --all-files
```

### Skipping hooks (not recommended)

If you need to commit without running hooks:
```bash
git commit --no-verify
```

This can be done to save/share work without needing to pass the commit
hooks. They will need to be passed eventually.
