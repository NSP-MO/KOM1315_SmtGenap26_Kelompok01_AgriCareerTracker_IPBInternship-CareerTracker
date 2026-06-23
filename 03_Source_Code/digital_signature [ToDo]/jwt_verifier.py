import os
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_for_demo_only")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def decode_token(token: str) -> dict:
    """
    Memverifikasi Digital Signature pada JWS/JWT Token.
    Fungsi ini merepresentasikan fitur Integritas & Autentikasi.
    """
    try:
        # jwt.decode akan secara otomatis mengecek Validitas Digital Signature
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(f"[VERIFICATION FAILED] JWTError: {e} - Token tidak valid atau Signature rusak.")
        return None

if __name__ == "__main__":
    pass
