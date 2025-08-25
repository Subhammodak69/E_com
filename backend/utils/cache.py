from datetime import datetime, timedelta

# In-memory OTP store
otp_cache = {}

def store_otp_in_memory(user_id: int, otp: str, ttl_minutes: int = 5):
    expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
    otp_cache[user_id] = (otp, expires_at)

def get_otp(user_id: int) -> str:
    record = otp_cache.get(user_id)
    if not record:
        return None
    otp, expires_at = record
    if datetime.utcnow() > expires_at:
        del otp_cache[user_id]  # Expired, clean up
        return None
    return otp

def delete_otp(user_id: int):
    otp_cache.pop(user_id, None)
