import psutil
from datetime import datetime
from typing import Dict, Any

class SystemMonitor:
    def __init__(self):
        self.thresholds = {
            'cpu_percent': 80.0,  # CPU使用率阈值
            'memory_percent': 80.0  # 内存使用率阈值
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        return {
            'timestamp': datetime.now(),
            'cpu_percent': cpu_percent,
            'memory_total': memory.total,
            'memory_available': memory.available,
            'memory_percent': memory.percent
        }
    
    def check_thresholds(self, system_info: Dict[str, Any]) -> Dict[str, bool]:
        """检查是否超过阈值"""
        return {
            'cpu_alert': system_info['cpu_percent'] > self.thresholds['cpu_percent'],
            'memory_alert': system_info['memory_percent'] > self.thresholds['memory_percent']
        }
    
    def set_threshold(self, metric: str, value: float) -> None:
        """设置监控阈值"""
        if metric in self.thresholds:
            self.thresholds[metric] = value