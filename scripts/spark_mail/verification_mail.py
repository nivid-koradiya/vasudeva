import smtplib
from email.mime.text import MIMEText
import environ

env = environ.Env()
environ.Env.read_env()

def send_email(subject,recipients,data):
    password = env('MAIL_PASSWORD')
    sender = env("MAIL_ID")
    body=''
    with open('scripts/spark_mail/templates/verification_mail.html','r') as f:
        body = f.read()
        # print(body)
    try:
        body = body.replace('**id**',data['id'])
    except:
        pass
    try:    
        body = body.replace('**url**',data['url'])
    except:
        pass
    msg = MIMEText(body,'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()
    print(f"mail_sent tp + {recipients}")
