import smtplib
from email.mime.text import MIMEText


class qSMTP():
    def __init__(self, p1="", p2="", smtp='smtp.163.com', port=25):
        super().__init__()
        if p1 == "" and p2 == "":
            p1 = 'zwy110120119@163.com'
            p2 = 'YQCOOZOICLDOAHHB'  # 授权码
        if p1 == "zwy" and p2 == "qwerty123":
            p1 = 'zwy110120119@163.com'
            p2 = 'YQCOOZOICLDOAHHB'  # 授权码
        self.p1 = p1
        self.p2 = p2
        self.smtp = smtp
        self.port = port
        self.s = None

    @classmethod
    def waitSend(cls,func,content="test",subject="163SMTP",msg_to="2181778692@qq.com"):
        func()
        cls.quickSend(content="test",subject="163SMTP",msg_to="2181778692@qq.com")

    def wait_send(self,func,content="test", subject="163SMTP", msg_to="2181778692@qq.com", callback={}):
        func()
        self.send(content="test", subject="163SMTP", msg_to="2181778692@qq.com", callback={})

    def send(self, content="test", subject="163SMTP", msg_to="2181778692@qq.com", callback={}):
        """
        callback is a dict 
        and have a parameter called self
        """
        if "beforelogin" in callback:
            callback['beforelogin'](self)

        self.s = smtplib.SMTP(self.smtp, self.port)
        self.s.login(self.p1, self.p2)

        if "beforesend" in callback:
            callback['before'](self,content,subject)

        
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.p1
        msg['To'] = msg_to
        self.s.sendmail(self.p1, msg_to, msg.as_string())
        
        if "aftersend" in callback:
            pass
        print("发送成功!!!")

    def __del__(self):
        if self.s:
            self.s.quit()
        del self

    @classmethod
    def quickSend(cls,content="test",subject="163SMTP",msg_to="2181778692@qq.com"):

        qsmtp = qSMTP()
        qsmtp.send(content,subject,msg_to)

def quickSend(content="test",subject="163SMTP",msg_to="2181778692@qq.com"):
    mySTMP = qSMTP()
    mySTMP.send(content,subject,msg_to)

# if __name__ == "__main___":
# mySTMP = qSMTP()
# mySTMP.send()
# qSMTP.quickSend()