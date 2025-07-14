import smtplib
from email.message import EmailMessage
from app.config import DevConfig
def send_reset_code(email, code):
    msg = EmailMessage()
    msg['Subject'] = 'Your Password Reset Code'
    msg['From'] = DevConfig.MAIL_DEFAULT_SENDER
    msg['To'] = email
    msg.set_content(f"Your 6-digit reset code is: {code}\nValid for 15 minutes.")

    with smtplib.SMTP(DevConfig.MAIL_SERVER, DevConfig.MAIL_PORT) as server:
        server.starttls()
        server.login(DevConfig.MAIL_USERNAME, DevConfig.MAIL_PASSWORD)
        server.send_message(msg)
