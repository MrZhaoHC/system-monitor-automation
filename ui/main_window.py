from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtCore import QThread, Signal
from .ui_main_window import Ui_MainWindow
from modules.system_monitor import SystemMonitor
from modules.file_manager import FileManager

class FileManagerThread(QThread):
    # 定义信号
    scan_completed = Signal(list)  # 扫描完成信号
    clean_completed = Signal(dict)  # 清理完成信号
    
    def __init__(self, file_manager):
        super().__init__()
        self.file_manager = file_manager
        self.task = None
        self.running = True
        self.scanning = False

    def run(self):
        try:
            if self.task == 'scan':
                self.scanning = True
                result = self.file_manager.scan_temp_files()
                if self.running:  # 只在未被中断时发送结果
                    self.scan_completed.emit(result)
            elif self.task == 'clean':
                result = self.file_manager.clean_old_files()
                self.clean_completed.emit(result)
        except Exception as e:
            print(f"未能启动文件管理线程: {str(e)}")
        finally:
            self.task = None
            self.running = True
            self.scanning = False

    def scan_files(self):
        if not self.isRunning():
            self.task = 'scan'
            self.start()

    def clean_files(self):
        if not self.isRunning():
            self.task = 'clean'
            self.start()

    def stop(self):
        self.running = False
        self.wait()

    def stop_scanning(self):
        if self.scanning:
            self.stop()

class SystemMonitorThread(QThread):
    # 定义信号
    system_info_updated = Signal(dict)
    alerts_updated = Signal(dict)
    
    def __init__(self, system_monitor):
        super().__init__()
        self.system_monitor = system_monitor
        self.running = True
    
    def run(self):
        while self.running:
            # 获取系统信息
            system_info = self.system_monitor.get_system_info()
            alerts = self.system_monitor.check_thresholds(system_info)
            
            # 发送信号
            self.system_info_updated.emit(system_info)
            self.alerts_updated.emit(alerts)
            
            # 休眠1秒
            self.msleep(1000)
    
    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 加载UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 初始化系统监控器
        self.system_monitor = SystemMonitor()
        
        # 初始化文件管理器
        self.file_manager = FileManager()
        
        # 初始化UI组件
        self._init_ui()
        
        # 创建并启动监控线程
        self.monitor_thread = SystemMonitorThread(self.system_monitor)
        self.monitor_thread.system_info_updated.connect(self.update_system_info)
        self.monitor_thread.alerts_updated.connect(self.update_alerts)
        self.monitor_thread.start()

        # 初始化文件管理器线程
        self.file_manager_thread = FileManagerThread(self.file_manager)
        self.file_manager_thread.scan_completed.connect(self._on_scan_completed)
        self.file_manager_thread.clean_completed.connect(self._on_clean_completed)

    def _init_ui(self):
        """初始化UI组件"""
        # 设置初始阈值
        self.ui.cpuThresholdSpinBox.setValue(int(self.system_monitor.thresholds['cpu_percent']))
        self.ui.memoryThresholdSpinBox.setValue(int(self.system_monitor.thresholds['memory_percent']))
        
        # 连接阈值变化信号
        self.ui.cpuThresholdSpinBox.valueChanged.connect(
            lambda value: self.system_monitor.set_threshold('cpu_percent', float(value))
        )
        self.ui.memoryThresholdSpinBox.valueChanged.connect(
            lambda value: self.system_monitor.set_threshold('memory_percent', float(value))
        )
        
        # 连接文件管理器相关信号
        self.ui.addTempDirButton.clicked.connect(self._add_temp_directory)
        self.ui.removeTempDirButton.clicked.connect(self._remove_temp_directory)
        self.ui.fileAgeThresholdSpinBox.valueChanged.connect(
            lambda value: self.file_manager.set_age_threshold(value)
        )
        self.ui.scanFilesButton.clicked.connect(self._scan_temp_files)
        self.ui.cleanFilesButton.clicked.connect(self._clean_old_files)
    
    def _add_temp_directory(self):
        """添加临时目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择临时文件目录")
        if directory:
            self.file_manager.add_temp_directory(directory)
            self.ui.tempDirListWidget.addItem(directory)
    
    def _remove_temp_directory(self):
        """移除临时目录"""
        current_item = self.ui.tempDirListWidget.currentItem()
        if current_item:
            directory = current_item.text()
            self.file_manager.temp_directories.remove(directory)
            self.ui.tempDirListWidget.takeItem(self.ui.tempDirListWidget.row(current_item))
    
    def _scan_temp_files(self):
        """扫描临时文件"""
        if self.file_manager_thread.scanning:
            # 如果正在扫描，则停止扫描
            self.file_manager_thread.stop_scanning()
            self.ui.scanFilesButton.setText("扫描文件")
            self.ui.scanResultTextEdit.setText("扫描已停止")
        else:
            # 开始扫描
            self.ui.scanFilesButton.setText("停止")
            self.ui.scanResultTextEdit.setText("正在扫描...")
            self.file_manager_thread.scan_files()

    def _on_scan_completed(self, temp_files):
        """处理扫描完成信号"""
        self.ui.scanFilesButton.setText("扫描文件")  # 恢复按钮文本
        result_text = []
        total_size = 0
        
        for file_info in temp_files:
            size_mb = file_info['size'] / (1024 * 1024)
            result_text.append(f"文件: {file_info['path']}")
            result_text.append(f"大小: {size_mb:.2f} MB")
            result_text.append(f"修改时间: {file_info['modified_time']}\n")
            total_size += file_info['size']
        
        result_text.append(f"\n总文件数: {len(temp_files)}")
        result_text.append(f"总大小: {total_size / (1024 * 1024):.2f} MB")
        
        self.ui.scanResultTextEdit.setText("\n".join(result_text))
        self.ui.scanFilesButton.setEnabled(True)
    
    def _clean_old_files(self):
            """清理旧文件"""
            if not self.file_manager_thread.isRunning():
                self.ui.cleanFilesButton.setEnabled(False)  # 禁用按钮防止重复操作
                self.ui.scanResultTextEdit.setText("正在清理...")
                self.file_manager_thread.clean_files()

    def _on_clean_completed(self, result):
        """处理清理完成信号"""
        cleaned_size_mb = result['bytes_cleaned'] / (1024 * 1024)
        result_text = f"清理完成\n已清理文件数: {result['files_cleaned']}\n清理空间: {cleaned_size_mb:.2f} MB"
        self.ui.scanResultTextEdit.setText(result_text)
        self.ui.cleanFilesButton.setEnabled(True)  # 重新启用按钮
    
    def update_system_info(self, system_info):
        """更新系统信息显示"""
        # 更新CPU信息
        cpu_percent = system_info['cpu_percent']
        self.ui.cpuProgressBar.setValue(int(cpu_percent))
        self.ui.cpuPercentLabel.setText(f"{cpu_percent:.1f}%")
        
        # 更新内存信息
        memory_percent = system_info['memory_percent']
        self.ui.memoryProgressBar.setValue(int(memory_percent))
        self.ui.memoryPercentLabel.setText(f"{memory_percent:.1f}%")
    
    def update_alerts(self, alerts):
        """更新告警状态"""
        # 根据阈值设置进度条样式
        self.ui.cpuProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red; }" if alerts['cpu_alert'] else ""
        )
        self.ui.memoryProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red; }" if alerts['memory_alert'] else ""
        )
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止监控线程
        self.monitor_thread.stop()
        self.monitor_thread.wait()
        if self.file_manager_thread.isRunning():
            self.file_manager_thread.stop()
        super().closeEvent(event)