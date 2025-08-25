import smtplib
from email.mime.text import MIMEText
from credentials import *

def send_otp_email(to_email: str, otp: str):
    msg = MIMEText(f"Your OTP for Shopy is: {otp}")
    msg["Subject"] = "Shopy OTP Verification"
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = to_email

    with smtplib.SMTP(EMAIL_HOST, 587) as server:
        server.starttls()  # ✅ Required for Gmail
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)
