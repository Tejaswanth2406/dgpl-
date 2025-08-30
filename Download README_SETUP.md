# Setup & Run Instructions — Secure API and JWT Attack

This file provides step-by-step instructions to set up, run, and test the Secure API (`secure_api.py`) and the JWT attack illustration (`jwt_attack.py`). Follow these steps on a local machine (Linux/macOS) or WSL on Windows.

---

## Prerequisites

- Python 3.8+ installed and available as `python3`
- `git` (if you cloned the repo)
- Recommended: `virtualenv` or Python `venv`
- Optional: `docker` and `docker-compose` (if you plan to containerize)

---

## 1. Clone the repository (if not already)

```bash
git clone https://github.com/Tejaswanth2406/dgpl-
cd dgpl-ctf-assignment   # or the directory name you used
```

If you already have the files locally, skip this step.

---

## 2. Create and activate a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

---

## 3. Install dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

`requirements.txt` should include:
- fastapi
- uvicorn
- pyjwt
- passlib[bcrypt]

---

## 4. Environment configuration

For secure usage, do not use hardcoded secrets. Set the `SECRET_KEY` environment variable before running the API.

On macOS / Linux:

```bash
export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

On Windows (PowerShell):

```powershell
$env:SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(48))")
```

The `secure_api.py` file contains a `SECRET_KEY` variable. You can modify it to read from the environment instead of using the hardcoded string:

```python
import os
SECRET_KEY = os.getenv("SECRET_KEY", "replace_with_strong_secret")
```

Make sure to set `SECRET_KEY` in your environment before starting uvicorn.

---

## 5. Run the Secure API (FastAPI)

Start the server with `uvicorn`:

```bash
uvicorn secure_api:app --reload --port 8000
```

The API will be available at: `http://127.0.0.1:8000`

Open `http://127.0.0.1:8000/docs` to view the automatic API documentation (Swagger UI).

---

## 6. Register a test user

Using `curl` (or Postman):

```bash
curl -X POST "http://127.0.0.1:8000/register"   -H "Content-Type: application/json"   -d '{"username":"alice","email":"alice@example.com","password":"StrongPassw0rd!"}'
```

Expected response: `{"msg":"user registered","username":"alice"}`

---

## 7. Login and obtain JWT

```bash
curl -X POST "http://127.0.0.1:8000/login"   -H "Content-Type: application/json"   -d '{"username":"alice","password":"StrongPassw0rd!"}'
```

Response will include `access_token`. Copy the token (JWT) for the next step.

---

## 8. Access protected endpoint

```bash
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/profile
```

Replace `<TOKEN>` with the `access_token` received from `/login`. Expected response contains user info.

---

## 9. Run the JWT attack script (illustration)

The attack script demonstrates two concepts:
- Forging an HS256 token when the signing secret is weak or known.
- Example construction of an unsigned `alg=none` token.

Run:

```bash
python3 jwt_attack.py
```

The script prints:
- A valid token created with a weak secret.
- A forged token setting `role=admin`.
- The decoded verification of the forged token using the same weak secret (to show how verification would succeed when secret is known).
- An `alg=none` unsigned token example.

---

## 10. How to demonstrate the vulnerability against the API

**Scenario:** If the API uses a weak secret (e.g., `secret`) and accepts HS256 tokens, an attacker who guesses the secret can forge tokens that the API will accept.

1. Ensure the API `SECRET_KEY` is the weak secret (for demonstration only).
2. Run the attack script (it will produce a forged token).
3. Use the forged token to call the protected endpoint:

```bash
curl -H "Authorization: Bearer <FORGED_TOKEN>" http://127.0.0.1:8000/profile
```

If the API uses the same weak secret and HS256, the request will be authorized and return profile information for the `sub` claim in the forged token.

**Important:** This is for educational/testing purposes only. Do not use these techniques on systems you do not own or have permission to test.

---

## 11. Converting REPORT.md to REPORT.pdf

Option A: Using `pandoc` (recommended)

```bash
pandoc REPORT.md -o REPORT.pdf
```

Option B: Use any Markdown editor or VS Code and print to PDF.

---

## 12. Optional: Dockerfile (quick example)

Create a `Dockerfile` for the API:

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV SECRET_KEY=replace_with_secure_value
EXPOSE 8000
CMD ["uvicorn", "secure_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t secure-api .
docker run -e SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')" -p 8000:8000 secure-api
```

---

## 13. Testing & Validation checklist

- Verify that passwords are stored as hashed values (not plaintext).
- Verify that tokens include `exp` claim and that expired tokens are rejected.
- Verify that changing `SECRET_KEY` invalidates previously issued tokens.
- Verify that unsigned `alg=none` tokens are rejected by the verification logic.
- Validate `aud` and `iss` claims if applicable.

---

## 14. Clean up

Stop `uvicorn` (Ctrl+C) or stop the Docker container.

Deactivate virtual environment:

```bash
deactivate
```

---

## Notes and Security Reminders

- Never commit secrets or credentials to version control.
- Use environment variables or secret managers for production secrets.
- Use HTTPS in production.
- Consider implementing refresh tokens and token revocation for higher security scenarios.

---

