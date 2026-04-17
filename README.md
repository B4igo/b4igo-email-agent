# b4igo-email-agent


## Setup

### Backend
Install the requirements (it's recommended to create a pyenv or conda environment first).
 ```bash
   pip install -r backend/requirements.txt
   ```
Install the git hooks:
   ```bash
   pre-commit install
   ```

### AccountManager microservice (internal)
Run the dedicated account manager server separately from the backend:
```bash
pip install -r account-manager/requirements.txt
python3 account-manager/account_manager_app.py
```

Optional environment variables:
- `B4IGO_ACCOUNT_MANAGER_PORT` (default `5100`)
- `B4IGO_ACCOUNT_DB_PATH` (default `email_agent.db`)
- `B4IGO_ACCOUNT_MANAGER_TOKEN` (if set, required in header `X-Internal-Service-Token`)

The backend (`backend/app.py`) calls this internal service through `B4IGO_ACCOUNT_MANAGER_URL` (default `http://127.0.0.1:5100`).

### Frontend
Open the terminal in the `frontend` folder and run npm install
to install the frontend packages (assuming that npm is already installed)
```bash
   npm i
```

Then use npm run dev to run the frontend:
```bash
   npm run dev
```

To run the frontend as an extension:
1. Open a terminal in `frontend` and build the app:
   ```bash
   npm run build
   ```
2. Open your Chromium-based browser (Chrome, Edge, etc.) and go to `chrome://extensions/` (or `edge://extensions/`). 
3. Turn on Developer mode in the top right corner. 
4. Click Load unpacked. 
5. Select the `frontend/dist` folder.


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
