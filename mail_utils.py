from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.utils import formataddr
import os
import smtplib
from email.header import Header

def send_mail():
    message = MIMEMultipart()
    message['To'] = formataddr(('test', '1375472577@qq.com'))
    message['From'] = formataddr(('book_feeder', '1375472577@qq.com'))
    message['Subject'] = '[book_feeder] Here are books you may like!'
    body = "Here are the books you may like!"
    message.attach(MIMEText(body, 'plain'))

    # 遍历特定目录下的所有文件
    directory = './downloads'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):  # 确保是文件而不是目录
            with open(file_path, "rb") as attachment_file:  # 以二进制模式打开文件
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())  # 设置附件内容
                encode_base64(part)  # 对附件内容进行 Base64 编码
                # 编码文件名
                encoded_filename = Header(filename, 'utf-8').encode()
                part.add_header('Content-Disposition', f'attachment; filename="{encoded_filename}"')
                message.attach(part)  # 将附件添加到邮件中
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login('1375472577@qq.com','gufdajxzlegwjeic')
    server.sendmail('1375472577@qq.com', ['1375472577@qq.com'], message.as_string())
    server.quit()

send_mail()