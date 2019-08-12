import smtplib, datetime, time
from email.mime.text import MIMEText
from email.header import Header


class SendEmail:
    def __init__(self):
        self.mail_host = "118.242.16.254"  # 设置服务器
        self.mail_user = "uding"  # 用户名
        self.mail_pass = "7ysg%3ki"  # 口令
        self.sender = 'uding@quatek.com.cn'

    def send(self, email, subject, txt):
        """
        :param email: 邮箱地址   ['ding1991aswsd@163.com', 'ding1991aswsd@163.com']
        :param subject: 邮箱标题
        :param txt: 邮件内容  html 格式
        :return:
        """
        # receivers = ['ding1991aswsd@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        receivers = email
        mail_msg = txt
        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = Header("QUATEK")
        message['To'] = Header("")
        message['Subject'] = Header(subject, 'utf-8')

        now_time = time.strftime("%a, %d %b %Y %H:%M:%S +0800", time.localtime())
        message['Date'] = Header(now_time)  # 设置发送时间

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, receivers, message.as_string())

            print(email, "邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


SendEmail().send(['625124155@qq.com'], '测试邮件', time.strftime("%a, %d %b %Y %H:%M:%S +0800", time.localtime()))