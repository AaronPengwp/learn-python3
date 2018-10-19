1、首先要确定好你的邮箱SMTP和POP3服务打开了

2、smtp_mail.py 实现发送的是纯文本内容

3、smtp_accessory_mail.py 实现发送的是附件和图片， MIMEMultipart(alternative)可以实现两种同时发送，兼容收件人使用的设备太古老，查看不了HTML邮件怎么办？
办法是在发送HTML的同时再附加一个纯文本，如果收件人无法查看HTML格式的邮件，就可以自动降级查看纯文本邮件。件人使用的设备太古老，查看不了HTML邮件怎么办？

4、pop3_acquire.py 实现邮件的接收

