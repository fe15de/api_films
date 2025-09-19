import hashlib, hmac, logging, os, json
from dotenv import load_dotenv

load_dotenv()

APP_SECRET = os.getenv("APP_SECRET")

def validate_signature(payload: str, signature: str) -> bool:
    expected_signature = hmac.new(
        APP_SECRET.encode("utf-8"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)