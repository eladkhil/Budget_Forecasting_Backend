from datetime import datetime, timedelta
from app.extensions import db
from app.models.User import User
from app.extensions import mail
from email.message import EmailMessage
import smtplib

def send_mail(to_email, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "yourapp@example.com"
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("yourapp@example.com", "app_password")
        server.send_message(msg)

from celery_worker import celery

@celery.task
def send_expiry_warnings():
    now = datetime.utcnow()
    in_3_days = now + timedelta(days=3)
    users = User.query.filter(User.password_expires.between(now, in_3_days)).all()

    for user in users:
        send_mail(
            user.email,
            "Your password is about to expire",
            f"Hi {user.name},\n\nYour password will expire on {user.password_expires.date()}. "
            f"Please log in and change it to avoid being locked out.\n\nThanks."
        )
