from flask_mail import Message
from flask import render_template
from myproject import mail
import os


def send_email(to, subject, template, **kwargs):
    msg = Message('[Flasky]' + subject,
            sender=os.environ.get('FLASKY_MAIL_SENDER'), recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
    