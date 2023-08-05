import smtplib, ssl
from flask import Flask,jsonify,request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)

class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "natalia.angiu@gmail.com"
        self.password = "rueyyhbsjgpezmqi"

    def send(self, email, subject, content):
        msg = MIMEMultipart()
        msg['From'] = self.sender_mail
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(content, 'plain'))

        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        service.sendmail(self.sender_mail, email, msg.as_string())

        service.quit()

def send_mail(email, subject, content):
    mail = Mail()
    mail.send(email, subject, content)

