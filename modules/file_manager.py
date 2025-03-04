import os
import shutil
from datetime import datetime, timedelta
from typing import List, Dict

class FileManager:
    def __init__(self):
        self.temp_directories = []
        self.file_age_threshold = 7  # 默认清理7天前的临时文件
    
    def add_temp_directory(self, directory: str) -> None:
        """添加需要监控的临时文件目录"""
        if os.path.exists(directory):
            self.temp_directories.append(directory)
    
    def scan_temp_files(self) -> List[Dict[str, any]]:
        """扫描临时文件"""
        temp_files = []
        for directory in self.temp_directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_stat = os.stat(file_path)
                    file_info = {
                        'path': file_path,
                        'size': file_stat.st_size,
                        'modified_time': datetime.fromtimestamp(file_stat.st_mtime)
                    }
                    temp_files.append(file_info)
        return temp_files
    
    def clean_old_files(self) -> Dict[str, int]:
        """清理过期的临时文件"""
        cleaned_count = 0
        cleaned_size = 0
        threshold_date = datetime.now() - timedelta(days=self.file_age_threshold)
        
        temp_files = self.scan_temp_files()
        for file_info in temp_files:
            if file_info['modified_time'] < threshold_date:
                try:
                    os.remove(file_info['path'])
                    cleaned_count += 1
                    cleaned_size += file_info['size']
                except OSError:
                    continue
        
        return {
            'files_cleaned': cleaned_count,
            'bytes_cleaned': cleaned_size
        }
    
    def set_age_threshold(self, days: int) -> None:
        """设置文件年龄阈值"""
        if days > 0:
            self.file_age_threshold = days