import smtplib, ssl
from email.message import EmailMessage
import os
from app.extensions import mail
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")          
SMTP_PASS = os.getenv("SMTP_PASS")

def send_reset_code(email, code):
    msg = EmailMessage()
    msg['Subject'] = 'Your Password Reset Code'
    msg['From'] = 'yourapp@example.com'
    msg['To'] = email
    msg.set_content(f"Your 6-digit reset code is: {code}\nValid for 15 minutes.")

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('elabendkhil9@gmail.com', 'hscf ucod vwdd uvxs')
        server.send_message(msg)
