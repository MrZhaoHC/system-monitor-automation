import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List

class NotificationManager:
    def __init__(self):
        self.smtp_settings = {
            'server': '',
            'port': 587,
            'username': '',
            'password': '',
            'use_tls': True
        }
        self.recipients = []
    
    def configure_smtp(self, settings: Dict[str, any]) -> None:
        """配置SMTP服务器设置"""
        self.smtp_settings.update(settings)
    
    def add_recipient(self, email: str) -> None:
        """添加收件人邮箱"""
        if email and '@' in email:
            self.recipients.append(email)
    
    def send_alert(self, subject: str, message: str) -> bool:
        """发送警报邮件"""
        if not all([self.smtp_settings['server'],
                   self.smtp_settings['username'],
                   self.smtp_settings['password'],
                   self.recipients]):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_settings['username']
            msg['To'] = ', '.join(self.recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.smtp_settings['server'],
                                 self.smtp_settings['port'])
            if self.smtp_settings['use_tls']:
                server.starttls()
            
            server.login(self.smtp_settings['username'],
                        self.smtp_settings['password'])
            
            server.send_message(msg)
            server.quit()
            return True
        except Exception:
            return False
    
    def send_system_alert(self, system_info: Dict[str, any],
                         alerts: Dict[str, bool]) -> bool:
        """发送系统警报"""
        if any(alerts.values()):
            subject = "系统资源警报"
            message = self._format_alert_message(system_info, alerts)
            return self.send_alert(subject, message)
        return False
    
    def _format_alert_message(self, system_info: Dict[str, any],
                           alerts: Dict[str, bool]) -> str:
        """格式化警报消息"""
        message = "系统资源使用警报:\n\n"
        if alerts.get('cpu_alert'):
            message += f"CPU使用率: {system_info['cpu_percent']}%\n"
        if alerts.get('memory_alert'):
            message += f"内存使用率: {system_info['memory_percent']}%\n"
        return message