# core/notifier.py

import smtplib
from email.mime.text import MIMEText
from config.settings import NOTIFICATION_METHOD

def notify(updates):
    if NOTIFICATION_METHOD == "email":
        send_email(updates)
    elif NOTIFICATION_METHOD == "slack":
        send_slack_message(updates)

def send_email(updates):
    msg = MIMEText(str(updates))
    msg['Subject'] = 'GitHub Repository Updates'
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('smtp.example.com') as server:
        server.login("user", "password")
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
