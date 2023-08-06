import smtplib
from random import randint
from email.header import Header
from email.mime.text import MIMEText
 
def Get(names, title, message):
    mail_host=names[0]
    mail_user=names[1]  
    mail_pass=names[2] 
    receivers = names[3]

    a = str(message[0] + " ")
    b = str(randint(100000, 999999))
    c = str(" " + message[1])
    message = MIMEText(str(a + b + c), 'plain', 'utf-8')

    message['From'] = Header(mail_user)
    message['To'] =  Header(receivers) 
    message['Subject'] = Header(title, 'utf-8') 
 
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        return b
    except smtplib.SMTPException:
        return False

# names:list(smpt_server_host, mail_user_name, smpt_password_code, receivers)
# "receivers"(from "names") can be a list or a string
# "title" is a string
# "message":list(front_message(in_fronnt_of_the_code), behind_message(behind_the_code))
