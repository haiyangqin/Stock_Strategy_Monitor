#!/usr/bin/python

#encoding=utf-8
import smtplib
import os
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
from email.mime.application import MIMEApplication

class Carry_files_EmailSender(object):
    def __init__(self):
        self.smtp_host = 'smtp.qq.com' # 发送邮件的smtp服务器(QQ邮箱："smtp.qq.com"，163邮箱："smtp.163.com")
        self.smtp_from_email = '420195048@qq.com' # 邮件发送者的邮箱
        self.smtp_pwd = 'qdrgbrqaprxccaih' # 邮件发送者的邮箱的授权码
        self.smtp_port = '465' # smtp邮箱的端口，默认是465

    def send_email(self, receivers, title, content,files_part=None):
        '''
        发送邮件
        param receivers: 收件人邮箱列表，格式["123@qq.com","123@163.com"]
        param title: 邮件主题，格式："邮件主题"
        param content:  邮件内容， 格式："邮件所说的内容"
        param files_part=None  发送的附件，默认不带附件，格式  r"E:\test.xlsx"
        '''
        msg= MIMEMultipart()
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        msg["From"] = self.smtp_from_email # 发件人
        msg["To"] = ",".join(receivers) # 收件人列表,转换成string，用逗号隔开
        msg["Subject"] = title # 邮件标题

        #上传指定文件构造附件
        if os.path.exists(files_part):
            filespart=MIMEApplication(open(files_part,'rb').read())
            file_name=files_part.split("\\")[-1] #获取文件名
            print("file_name=",file_name)
            filespart.add_header("Content-Disposition","attachment",filename=file_name) #file_name是显示附件的名字，可随便自定义
            msg.attach(filespart)

        else:
            print("加载的附件不存在,发送无附件邮件")

        try:
            SmtpSslClient = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) # 实例化一个SMTP_SSL对象
            Loginer = SmtpSslClient.login(self.smtp_from_email, self.smtp_pwd) # 登录smtp服务器
            print("登录结果：Loginer=", Loginer)  # loginRes =  (235, b'Authentication successful')
            if Loginer[0] == 235:
                print("登录成功，code=",Loginer[0])
                SmtpSslClient.sendmail(self.smtp_from_email, receivers, msg.as_string()) # 发件人，收件人列表，邮件内容
                print("mail has been send successfully,message:", msg.as_string())
                print("发送成功")
                SmtpSslClient.quit() # 退出邮箱
            else:
                print("邮件登录失败，发送失败。code=", Loginer[0], "message=", msg.as_string())
        except Exception as e:
            traceback.print_exc()
            print("邮件发送失败，报错信息：", e)

if __name__=="__main__":
    senders = Carry_files_EmailSender()
    senders.send_email(["420195048@qq.com"], "测试邮件发送的标题", "这是一个测试邮件发送的内容",r"C:\Users\hyqin\Desktop\my_test\test.txt")