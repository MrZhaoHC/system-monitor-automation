import os
from datetime import datetime

class FileManager:
    def __init__(self):
        self.temp_directories = []
        self.age_threshold = 7  # 默认7天
        self.scanning = True  # 添加扫描状态控制
    
    def add_temp_directory(self, directory):
        """添加临时目录"""
        if os.path.isdir(directory) and directory not in self.temp_directories:
            self.temp_directories.append(directory)
    
    def stop_scan(self):
        """停止扫描"""
        self.scanning = False
    
    def scan_temp_files(self):
        """扫描临时文件"""
        self.scanning = True
        temp_files = []
        for directory in self.temp_directories:
            if not self.scanning:  # 检查是否需要停止扫描
                break
            try:
                for root, _, files in os.walk(directory):
                    if not self.scanning:  # 检查是否需要停止扫描
                        break
                    for file in files:
                        if not self.scanning:  # 检查是否需要停止扫描
                            break
                        try:
                            file_path = os.path.join(root, file)
                            file_stat = os.stat(file_path)
                            # 使用try-except处理时间戳转换
                            try:
                                modified_time = datetime.fromtimestamp(file_stat.st_mtime)
                            except (OSError, ValueError) as e:
                                print(f"Error converting timestamp for {file_path}: {e}")
                                continue
                            
                            temp_files.append({
                                'path': file_path,
                                'size': file_stat.st_size,
                                'modified_time': modified_time
                            })
                        except OSError as e:
                            print(f"Error accessing file {file}: {e}")
                            continue
            except OSError as e:
                print(f"Error accessing directory {directory}: {e}")
                continue
        return temp_files
    
    def clean_old_files(self):
        """清理过期文件"""
        now = datetime.now()
        files_cleaned = 0
        bytes_cleaned = 0
        
        temp_files = self.scan_temp_files()
        for file_info in temp_files:
            try:
                file_age = (now - file_info['modified_time']).days
                if file_age >= self.age_threshold:
                    try:
                        os.remove(file_info['path'])
                        files_cleaned += 1
                        bytes_cleaned += file_info['size']
                    except OSError as e:
                        print(f"Error deleting file {file_info['path']}: {e}")
            except TypeError as e:
                print(f"Error calculating file age for {file_info['path']}: {e}")
        
        return {
            'files_cleaned': files_cleaned,
            'bytes_cleaned': bytes_cleaned
        }
    
    def set_age_threshold(self, days):
        """设置文件年龄阈值"""
        self.age_threshold = days