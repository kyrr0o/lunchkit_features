from src import mail
from flask_mail import Message

def send_mail(subject,sender,recipient,body):
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=[recipient]
    )
    msg.body = body
    mail.send(msg)