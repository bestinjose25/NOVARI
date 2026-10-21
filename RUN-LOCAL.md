# Run NOVARI locally

Install Node.js 24 LTS and Python 3.13. For a fresh clone, run from the project folder:

```powershell
npm.cmd ci
npm.cmd --prefix frontend ci
python -m venv backend/.venv
.\backend\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
Copy-Item backend/.env.example backend/.env
'VITE_API_BASE_URL=http://127.0.0.1:8001' | Set-Content frontend/.env.local
```

Fill in your own email settings in `backend/.env`. Then start both services:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-local.ps1
```

Open http://127.0.0.1:5173. The backend runs at http://127.0.0.1:8001.
Run the script once per session; the servers continue running in the background.
Logs are in `.local-tools`.

Development uses `backend/config/settings_local.py`, an isolated Python virtual environment,
and a local SQLite database. Without SMTP credentials, form emails are saved in
`backend/.local-emails/`. With SMTP credentials, emails are sent through your provider.
The frontend API URL is in `frontend/.env.local`.

To rebuild the frontend:

```powershell
npm.cmd --prefix frontend run build
```
