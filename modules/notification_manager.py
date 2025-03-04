import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from typing import Dict, List

class NotificationManager:
    def __init__(self):
        self.smtp_settings = {
            'smtp_server': 'smtp.163.com',  # 163邮箱服务器
            'smtp_port': 465,  # 使用SSL的端口
            'smtp_username': 'your_email@163.com',  # 替换为您的163邮箱
            'smtp_password': 'your_auth_code',  # 替换为您获取的授权码
            'use_tls': False  # 163邮箱使用SSL而不是TLS
        }
        self.recipients = []
        self.last_alert_time = None  # 记录上次发送告警的时间
        self.alert_interval = 600  # 告警间隔时间（秒），默认10分钟
    
    def configure_smtp(self, settings: Dict[str, any]) -> None:
        """配置SMTP服务器设置"""
        self.smtp_settings.update(settings)
        if 'alert_interval' in settings:
            self.alert_interval = settings['alert_interval'] * 60  # 将分钟转换为秒
    
    def add_recipient(self, email: str) -> None:
        """添加收件人邮箱"""
        if email and '@' in email:
            self.recipients.append(email)
    
    def send_alert(self, subject: str, message: str) -> bool:
        """发送警报邮件"""
        current_time = datetime.now()

        # 检查是否需要发送告警（是否超过间隔时间）
        if self.last_alert_time and (current_time - self.last_alert_time).total_seconds() < self.alert_interval:
            return False
            
        if not all([self.smtp_settings['smtp_server'],
                   self.smtp_settings['smtp_username'],
                   self.smtp_settings['smtp_password'],
                   self.recipients]):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_settings['smtp_username']
            msg['To'] = ', '.join(self.recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # 使用SSL连接
            server = smtplib.SMTP_SSL(self.smtp_settings['smtp_server'],
                                   self.smtp_settings['smtp_port'])
            
            server.login(self.smtp_settings['smtp_username'],
                        self.smtp_settings['smtp_password'])
            
            server.send_message(msg)
            server.quit()
            self.last_alert_time = current_time  # 更新最后发送时间
            return True
        except Exception as e:
            print(f"发送邮件失败: {str(e)}")  # 添加错误日志
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