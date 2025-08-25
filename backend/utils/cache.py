from datetime import datetime, timedelta
import random
from typing import Optional
import uuid
# In-memory OTP store with expiry support
otp_cache = {}

def store_otp_in_memory(temp_id: str, otp: str, ttl_seconds: int = 300):
    expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    otp_cache[temp_id] = (otp, expires_at)

def get_otp(temp_id: str) -> Optional[str]:
    record = otp_cache.get(temp_id)
    if not record:
        print(f"OTP cache miss for temp_id {temp_id} at {datetime.utcnow()}")
        return None
    otp, expires_at = record
    if datetime.utcnow() > expires_at:
        print(f"OTP expired for temp_id {temp_id} at {datetime.utcnow()}")
        del otp_cache[temp_id]  # Expired, clean up
        return None
    print(f"OTP found for temp_id {temp_id} at {datetime.utcnow()}")
    return otp


def delete_otp(temp_id: str):
    otp_cache.pop(temp_id, None)

def generate_temp_user_id() -> str:
    return uuid.uuid4().hex[:16]

def generate_otp() -> str:
    return str(random.randint(100000, 999999))
