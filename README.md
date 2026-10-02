# SynthGEN

## Overview

SynthGEN is a full-stack application for generating synthetic tabular datasets
from a plain-language description. Google Gemini proposes a structured schema;
Faker and Python's random utilities generate the records, and Pandas builds the
dataset. It is a software project that uses an external AI API, not a trained
machine-learning model.

## Features

- Register and log in with JWT authentication and hashed passwords.
- Describe a dataset and generate up to 5,000 rows per request.
- Preview the first 20 records and inspect the proposed column schema.
- Download a generated dataset as CSV.
- View and delete your own generation history.
- Update your account name and email.

## Architecture

```text
React / Vite / Axios frontend
             |
          Flask API ----- SQLite: users and generation metadata
             |
      Gemini: schema proposal
             |
  Faker + random: synthetic values
             |
      Pandas: dataset / CSV
```

## Tech Stack

| Layer | Implementation |
| --- | --- |
| Frontend | React, Vite, Axios, React Router, CSS and inline styles |
| Backend | Python, Flask, Flask-CORS, Flask-SQLAlchemy, Flask-JWT-Extended |
| Configuration | python-dotenv |
| AI and data | Google Gemini API (`google-generativeai`), Faker, Pandas |
| Database | SQLite |
| Verification | pytest, ESLint, GitHub Actions |

There is no FastAPI, Uvicorn, Tailwind, or JSON file export in this implementation.
Pydantic is a transitive SDK dependency, not the backend framework.

## How It Works

1. The user registers or logs in. The frontend stores the JWT in local storage
   and sends it in the `Authorization: Bearer` header for protected requests.
2. The frontend sends a description and row count to `/api/generate`.
3. Gemini (`gemini-2.5-flash`) interprets the description and returns column
   names, types, and optional numeric bounds or choices. Provider output is
   validated before use.
4. Faker (using the `en_IN` locale) generates values such as names, addresses,
   emails, and dates. Python random utilities generate numbers and choices.
5. Pandas creates the table. The API returns a preview and schema; SQLite records
   the user's prompt, row count, column count, filename, and timestamp.
6. `/api/download` performs a **new generation** for the description and returns
   CSV. It does not download a stored copy of the preview dataset. Formula-like
   strings are escaped for safer spreadsheet use.

SQLite stores users and generation metadata, not the generated records or CSV files.

## Local Setup

Use Python 3.12 and Node.js 24 LTS with npm. The commands below use PowerShell.

```powershell
git clone https://github.com/manthan3502/SynthGEN.git
cd SynthGEN
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements-lock.txt -r backend/requirements-dev.txt
Copy-Item backend/.env.example backend/.env
```

Edit `backend/.env` privately. Set `SECRET_KEY` to a locally generated random
value of at least 32 characters. Configure your own `GEMINI_API_KEY` only for
live generation. Never commit these values or put them in frontend variables.
No real API key is required to run tests.

Start the backend:

```powershell
cd backend
..\.venv\Scripts\python.exe app.py
```

In a separate terminal, start the frontend:

```powershell
cd SynthGEN/frontend
npm ci
Copy-Item .env.example .env
npm run dev
```

The development frontend normally runs at `http://localhost:5173` and the
backend at `http://localhost:5000`. SQLite tables are created at application
startup in the ignored `backend/instance/dataforge.db` file. The Flask server
used here is for local development; this repository does not document a
production deployment.

On macOS/Linux, activate the virtual environment with `source .venv/bin/activate`
and use `python` in place of the Windows executable paths. Use `cp` to copy the
environment examples.

`backend/requirements.txt` pins the direct runtime dependencies;
`backend/requirements-lock.txt` pins their resolved dependency graph.
`backend/requirements-dev.txt` adds pytest. Frontend versions are recorded in
`frontend/package-lock.json`; install them with `npm ci`.

## Environment Variables

| Variable | Location | Behavior |
| --- | --- | --- |
| `GEMINI_API_KEY` | Backend only | Required for live schema generation; no default |
| `SECRET_KEY` | Backend only | Required signing secret, at least 32 characters; no fallback |
| `CORS_ORIGINS` | Backend only | Comma-separated explicit origins; defaults to `http://localhost:5173,http://127.0.0.1:5173` |
| `VITE_API_BASE_URL` | Frontend | Defaults to `http://localhost:5000`; public in the built client |

`.env.example` files contain empty secret placeholders or public development
configuration. `.env` files, SQLite databases, caches, and build outputs are ignored.
Environment variables already set in the process take precedence over `.env`.
If Vite chooses another port, explicitly add its origin to `CORS_ORIGINS`.

## Testing

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest -c backend/pytest.ini backend/tests -q
cd frontend
npm run lint
npm run build
```

Backend tests use a temporary SQLite database and test-only signing credentials.
They mock schema generation, block network connections, and never load a real
`.env` file. Coverage includes registration, login, request validation,
JWT-protected routes, generation, CSV download, history isolation and deletion,
configuration, CORS, unsafe schemas, and private provider errors.

GitHub Actions installs dependencies, runs backend tests, and runs frontend lint
and build on pushes to `main` and pull requests. No Gemini credential or CI
secret is needed. There is no frontend `npm test` script.

## Security Notes

- Passwords use Werkzeug password hashing. JWTs use the configured backend secret.
- Generation history is scoped to the authenticated user, including deletion.
- CORS permits explicitly configured origins. It does not replace authentication.
- Provider exceptions are neither returned verbatim nor logged with their contents.
- The development server starts with debug mode disabled.
- Keep descriptions free of confidential data: descriptions are sent to Gemini
  and recorded in the local generation history.
- An earlier committed API key was revoked. Environment files, the historical
  database, and Python caches were removed from reachable project history.
  History rewriting cannot guarantee deletion from old clones, forks, reflogs,
  caches, or GitHub internal storage. Use a fresh clone after the rewrite.

## Limitations

- Records are synthetic examples, not measured observations or validated domain
  simulations. Independent random columns may not preserve real-world correlations.
- Generation depends on external model availability, quota, and account pricing.
  No universal free-use or performance guarantee is made.
- CSV downloads regenerate the data, so they can differ from the preview.
  History contains metadata only and has no saved-dataset re-download action.
- JSON is used for API responses; JSON **file export** is not implemented.
- The current Gemini integration retains the existing legacy
  `google-generativeai` SDK. Its maintenance and model availability need review
  before a future deployment.
- JWTs remain in browser local storage. There is no rate limiting, email
  verification, password reset, or token revocation flow. Further hardening is
  needed before public hosting.
- The repository does not provide a fixed random seed or guarantee identical
  generated records across runs. Installation and automated tests are reproducible.

## Future Improvements

- Retain generated datasets so downloads match previews.
- Add optional domain constraints and seeded generation.
- Add more export formats, including JSON file export.
- Improve authentication hardening and evaluate a maintained Gemini SDK.

## Author

Manthan Karekar — B.Tech Computer Science Engineering, DES Pune University.

Licensed under the [MIT License](LICENSE).
