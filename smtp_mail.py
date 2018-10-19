# !usr/bin/env  python
# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 输入Email地址和口令
from_addr =input("From: ")
password = input('Password: ') #这个是授权码，不是密码
#输入收件人地址
to_addr = input('To: ')
#输入SMTP服务器地址:
smtp_server = input('SMTP server: ') #'smtp.163.com'

msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)#_format_addr()来格式化一个邮件地址。注意不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码。
msg['To'] = _format_addr('管理员 <%s>' % to_addr)#msg['To']接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可。
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()#标题

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)#set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()