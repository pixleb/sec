# email imports
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# misc imports
import asyncio, sys

class Main:
    def __init__(self):
        self.sender: str = 'dmulykov@outlook.com'
        self.password: str = 'Animudesu1'
            
    async def async_send_mail(self, receiver: str, subject: str, text: str) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = receiver
        msg['Subject'] = subject
        
        msg.attach(MIMEText(text))
        
        server = smtplib.SMTP(host = 'smtp-mail.outlook.com', port = 587)
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, receiver, msg.as_string())
        server.close() 
    
    def send_mail(self, receiver: str, subject: str, text: str) -> None:
        v: sys.version_info = sys.version_info
        v_major: int = v.major
        v_minor: int = v.minor
            
        if v_major != 3 or v_minor < 4: raise SystemError('Incompatible Python version (requires Python 3.4 + )')
        elif v_minor < 8:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.async_send_mail(receiver, subject, text))
            return 
        asyncio.run(self.async_send_mail(receiver, subject, text))

        