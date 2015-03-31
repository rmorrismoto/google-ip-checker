import smtplib
import os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text="", cc=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Cc'] = COMMASPACE.join(cc)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to+cc, msg.as_string())
    smtp.close()
