import smtplib
import email.utils
from email.mime.text import MIMEText
def send_mail():
    message = MIMEText("None")
    message['To'] = email.utils.formataddr(('test', '1375472577@qq.com'))
    message['From'] = email.utils.formataddr(('book_feeder', '1375472577@qq.com'))
    message['Subject'] = '[book_feeder]Here are books you may like!'
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login('1375472577@qq.com','gufdajxzlegwjeic')
    server.set_debuglevel(True)
    server.sendmail('1375472577@qq.com',['1375472577@qq.com'],msg=message.as_string())
    server.quit()
