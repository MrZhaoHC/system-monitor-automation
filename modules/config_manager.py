import json
import os

class ConfigManager:
    def __init__(self):
        self.config_file = 'config.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
        return self._get_default_config()
    
    def _get_default_config(self):
        """获取默认配置"""
        return {
            'system_monitor': {
                'cpu_percent': 80,
                'memory_percent': 80
            },
            'file_manager': {
                'temp_directories': []
            },
            'notification': {
                'smtp_server': '',
                'smtp_port': 587,
                'smtp_username': '',
                'smtp_password': '',
                'use_tls': True,
                'recipients': [],
                'alert_interval': 10
            }
        }
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False
    
    def get_system_monitor_config(self):
        """获取系统监控配置"""
        return self.config['system_monitor']
    
    def set_system_monitor_config(self, cpu_percent=None, memory_percent=None):
        """设置系统监控配置"""
        if cpu_percent is not None:
            self.config['system_monitor']['cpu_percent'] = cpu_percent
        if memory_percent is not None:
            self.config['system_monitor']['memory_percent'] = memory_percent
        self.save_config()
    
    def get_temp_directories(self):
        """获取临时目录列表"""
        return self.config['file_manager']['temp_directories']
    
    def add_temp_directory(self, directory):
        """添加临时目录"""
        if directory not in self.config['file_manager']['temp_directories']:
            self.config['file_manager']['temp_directories'].append(directory)
            self.save_config()
    
    def remove_temp_directory(self, directory):
        """移除临时目录"""
        if directory in self.config['file_manager']['temp_directories']:
            self.config['file_manager']['temp_directories'].remove(directory)
            self.save_config()
    
    def get_notification_config(self):
        """获取通知配置"""
        return self.config['notification']
    
    def set_notification_config(self, settings):
        """设置通知配置"""
        self.config['notification'].update(settings)
        self.save_config()
    
    def add_recipient(self, email):
        """添加收件人"""
        if email not in self.config['notification']['recipients']:
            self.config['notification']['recipients'].append(email)
            self.save_config()
    
    def remove_recipient(self, email):
        """移除收件人"""
        if email in self.config['notification']['recipients']:
            self.config['notification']['recipients'].remove(email)
            self.save_config()