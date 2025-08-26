import smtplib
from email.message import EmailMessage
from app.utils.notifier import emit_notification,save_notification
from app.utils.load_email import load_email_config
def send_reset_code(email, code):
    config = load_email_config()
    msg = EmailMessage()
    msg['Subject'] = 'Your Password Reset Code'
    msg['From'] = config['mail_default_sender']
    msg['To'] = email
    msg.set_content(f"Your 6-digit reset code is: {code}\nValid for 15 minutes.")

    with smtplib.SMTP( config['mail_server'],  config['mail_port']) as server:
        server.starttls()
        server.login( config['mail_username'],  config['mail_password'])
        server.send_message(msg)

def notify_users_about_action(action,users):
    config=load_email_config()
    print(config)
    save_notification(
                user_ids=[user.user_id for user in users],
                title="Nouvelle action",
                message=f"une nouvelle action vous est assignée :{action.description}"
            )
    for user in users:
        try:
            msg = EmailMessage()
            msg['Subject']="Nouvelle Action Assignée"
            msg['To']=user.email
            msg['From'] = config['mail_default_sender']
            msg.set_content(f"Bonjour {user.name},\n\nUne nouvelle action vous a été assignée :\n\n"
            f"- Description : {action.description}\n"
            f"- Statut : {action.statut}\n"
            f"- Date limite : {action.date_limite}\n\nMerci de prendre connaissance de cette tâche.")
            with smtplib.SMTP( config['mail_server'],  config['mail_port']) as server:
                server.starttls()
                server.login( config['mail_username'],  config['mail_password'])
                server.send_message(msg)
            emit_notification('nouvelle_notification',{
                'user_id':user.user_id,
                'title':"Nouvelle action",
                'message':f"{user.name},une nouvelle action vous est assignée :{action.description}",
                'is_read': False

            })
        except Exception as mail_err:
            print(f"Erreur envoi mail à {user.email} :", mail_err)

