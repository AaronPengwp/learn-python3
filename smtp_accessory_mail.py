# !usr/bin/env  python
# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64

import smtplib



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 输入Email地址和口令
from_addr = input("From: ")
password =  input('Password: ') #这个是授权码，不是密码
#输入收件人地址
to_addr = input('To: ')
#输入SMTP服务器地址:
smtp_server = input('SMTP server: ') #'smtp.163.com'
smtp_port = 25
ssl_port  = 587

#m邮件对象
msg = MIMEMultipart()#'alternative'
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)#_format_addr()来格式化一个邮件地址。注意不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码。
msg['To'] = _format_addr('管理员 <%s>' % to_addr)#msg['To']接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可。
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()



def mail():
    ret=True
    # 邮件正文是MIMEText:
    #1、以发送附件的方式
    #msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
    #2、发送图片只需按照发送附件的方式，先把邮件作为附件添加进去，然后，在HTML中通过引用src="cid:0"就可以把附件作为图片嵌入了。如果有多个图片，给它们依次编号，然后引用不同的cid:x即可。
    msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open('plane.jpg', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'jpg', filename='plane.jpg')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='plane.jpg')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
    try:
        #连接smtp服务器，明文/SSL/TLS三种方式，根据你使用的SMTP支持情况选择一种
        #普通方式，通信过程不加密
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)#可以打印出和SMTP服务器交互的所有信息。

        #tls加密方式，通信过程加密，邮件数据安全，使用正常的smtp端口
        # server = smtplib.SMTP(smtp_server,smtp_port)
        # server.set_debuglevel(True)
        # server.ehlo() #跟 ESMTP 邮件服务器 say hello
        # server.starttls()#将 smtp 连接切换到 tls 模式
        # server.ehlo()

        #纯粹的ssl加密方式，通信过程加密，邮件数据安全
        # server = smtplib.SMTP_SSL(smtp_server,ssl_port)
        # server.ehlo()


        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except Exception:
        ret =  False
    return ret

if __name__ == '__main__':
    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

'''
同时支持HTML和Plain格式
如果我们发送HTML邮件，收件人通过浏览器或者Outlook之类的软件是可以正常浏览邮件内容的，但是，如果收件人使用的设备太古老，查看不了HTML邮件怎么办？

办法是在发送HTML的同时再附加一个纯文本，如果收件人无法查看HTML格式的邮件，就可以自动降级查看纯文本邮件。

利用MIMEMultipart就可以组合一个HTML和Plain，要注意指定subtype是alternative：

msg = MIMEMultipart('alternative')
msg['From'] = ...
msg['To'] = ...
msg['Subject'] = ...

msg.attach(MIMEText('hello', 'plain', 'utf-8'))
msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
# 正常发送msg对象...
'''