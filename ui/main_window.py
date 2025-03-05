import os
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLineEdit
from PySide6.QtCore import QThread, Signal
from datetime import datetime
from .ui_main_window import Ui_MainWindow
from modules.system_monitor import SystemMonitor
from modules.file_manager import FileManager
from modules.notification_manager import NotificationManager
from modules.config_manager import ConfigManager
from modules.report_generator import ReportGenerator

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
        if self.scanning:
            self.file_manager.stop_scan()  # 通知文件管理器停止扫描
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

class ReportGeneratorThread(QThread):
    report_generated = Signal(str)  # 报告生成完成信号
    
    def __init__(self, report_generator, report_type, system_data, cleanup_data):
        super().__init__()
        self.report_generator = report_generator
        self.report_type = report_type
        self.system_data = system_data
        self.cleanup_data = cleanup_data
    
    def run(self):
        try:
            if self.report_type == 'pdf':
                filename = self.report_generator.generate_pdf_report(
                    self.system_data, self.cleanup_data)
            else:
                filename = self.report_generator.generate_html_report(
                    self.system_data, self.cleanup_data)
            self.report_generated.emit(filename)
        except Exception as e:
            print(f"生成报告失败: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 加载UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 加载样式表
        style_file = os.path.join(os.path.dirname(__file__), 'style.qss')
        with open(style_file, 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        
        # 初始化系统监控器
        self.system_monitor = SystemMonitor()
        self.system_monitor.thresholds = self.config_manager.get_system_monitor_config()
        
        # 初始化文件管理器
        self.file_manager = FileManager()
        
        # 初始化报告生成器
        self.report_generator = ReportGenerator()
        
        # 存储系统监控数据
        self.system_data = []
        self.cleanup_data = {'files_cleaned': 0, 'bytes_cleaned': 0}

        for directory in self.config_manager.get_temp_directories():
            self.file_manager.add_temp_directory(directory)
        
        # 初始化通知管理器
        self.notification_manager = NotificationManager()
        notification_config = self.config_manager.get_notification_config()
        self.notification_manager.configure_smtp(notification_config)
        for recipient in notification_config['recipients']:
            self.notification_manager.add_recipient(recipient)
        
        # 初始化UI组件
        self._init_ui()
        
        # 创建并启动监控线程
        self.monitor_thread = SystemMonitorThread(self.system_monitor)
        self.monitor_thread.system_info_updated.connect(self._update_system_info)
        self.monitor_thread.alerts_updated.connect(self._update_alerts)
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

        # 设置初始文件管理UI
        self.ui.cleanFilesButton.setEnabled(False)
        for directory in self.file_manager.temp_directories:
            self.ui.tempDirListWidget.addItem(directory)
            
        # 设置初始通知设置UI
        notification_config = self.config_manager.get_notification_config()
        self.ui.smtpServerLineEdit.setText(notification_config['smtp_server'])
        self.ui.smtpPortSpinBox.setValue(notification_config['smtp_port'])
        self.ui.smtpUsernameLineEdit.setText(notification_config['smtp_username'])
        self.ui.smtpPasswordLineEdit.setText(notification_config['smtp_password'])
        self.ui.useTlsCheckBox.setChecked(notification_config['use_tls'])
        self.ui.alertIntervalSpinBox.setValue(notification_config.get('alert_interval', 10))
        for recipient in notification_config['recipients']:
            self.ui.recipientsListWidget.addItem(recipient)
        
        # 连接阈值变化信号
        self.ui.cpuThresholdSpinBox.valueChanged.connect(
            lambda value: self._update_cpu_threshold(value)
        )
        self.ui.memoryThresholdSpinBox.valueChanged.connect(
            lambda value: self._update_memory_threshold(value)
        )
        
        # 连接文件管理器相关信号
        self.ui.addTempDirButton.clicked.connect(self._add_temp_directory)
        self.ui.removeTempDirButton.clicked.connect(self._remove_temp_directory)
        self.ui.fileAgeThresholdSpinBox.valueChanged.connect(
            lambda value: self.file_manager.set_age_threshold(value)
        )
        self.ui.scanFilesButton.clicked.connect(self._scan_temp_files)
        self.ui.cleanFilesButton.clicked.connect(self._clean_old_files)
        
        # 连接通知管理器相关信号
        self.ui.smtpServerLineEdit.textChanged.connect(self._update_smtp_settings)
        self.ui.smtpPortSpinBox.valueChanged.connect(self._update_smtp_settings)
        self.ui.smtpUsernameLineEdit.textChanged.connect(self._update_smtp_settings)
        self.ui.smtpPasswordLineEdit.textChanged.connect(self._update_smtp_settings)
        self.ui.useTlsCheckBox.stateChanged.connect(self._update_smtp_settings)
        self.ui.alertIntervalSpinBox.valueChanged.connect(self._update_smtp_settings)
        self.ui.addRecipientButton.clicked.connect(self._add_recipient)
        self.ui.removeRecipientButton.clicked.connect(self._remove_recipient)

        # 连接报告生成器相关信号
        self.ui.generateReportButton.clicked.connect(self._generate_report)
    
    def _add_temp_directory(self):
        """添加临时目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择临时文件目录")
        if directory:
            self.file_manager.add_temp_directory(directory)
            self.ui.tempDirListWidget.addItem(directory)
            self.config_manager.add_temp_directory(directory)
    
    def _remove_temp_directory(self):
        """移除临时目录"""
        current_item = self.ui.tempDirListWidget.currentItem()
        if current_item:
            directory = current_item.text()
            self.file_manager.temp_directories.remove(directory)
            self.ui.tempDirListWidget.takeItem(self.ui.tempDirListWidget.row(current_item))
            self.config_manager.remove_temp_directory(directory)
    
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
        self.ui.cleanFilesButton.setEnabled(False)

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
        self.ui.cleanFilesButton.setEnabled(True)
    
    def _clean_old_files(self):
        """清理旧文件"""
        if not self.file_manager_thread.isRunning():
            # 计算要清理的文件数量和总大小
            now = datetime.now()
            files_to_clean = 0
            total_size = 0
            for file_info in self.file_manager.cached_temp_files:
                try:
                    file_age = (now - file_info['modified_time']).days
                    if file_age >= self.file_manager.age_threshold:
                        files_to_clean += 1
                        total_size += file_info['size']
                except TypeError:
                    continue
            
            if files_to_clean > 0:
                # 显示确认对话框
                size_mb = total_size / (1024 * 1024)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Question)
                msg.setWindowTitle("确认清理")
                msg.setText(f"确定要清理以下文件吗？\n\n文件数量：{files_to_clean}\n总大小：{size_mb:.2f} MB")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                msg.setDefaultButton(QMessageBox.StandardButton.No)
                
                if msg.exec() == QMessageBox.StandardButton.Yes:
                    self.ui.cleanFilesButton.setEnabled(False)  # 禁用按钮防止重复操作
                    self.ui.scanResultTextEdit.setText("正在清理...")
                    self.file_manager_thread.clean_files()
            else:
                # 如果没有需要清理的文件，显示提示
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("提示")
                msg.setText("没有需要清理的文件")
                msg.exec()

    def _on_clean_completed(self, result):
        """处理清理完成信号"""
        cleaned_size_mb = result['bytes_cleaned'] / (1024 * 1024)
        result_text = f"清理完成\n已清理文件数: {result['files_cleaned']}\n清理空间: {cleaned_size_mb:.2f} MB"
        self.ui.scanResultTextEdit.setText(result_text)
        # 保存清理数据用于生成报告
        self.cleanup_data = result
    
    def _generate_report(self):
        """生成报告"""
        report_type = 'pdf' if self.ui.pdfRadioButton.isChecked() else 'html'
        print(report_type)
        
        # 创建并启动报告生成线程
        self.report_thread = ReportGeneratorThread(
            self.report_generator,
            report_type,
            self.system_data,
            self.cleanup_data
        )
        self.report_thread.report_generated.connect(self._on_report_generated)
        
        # 禁用生成按钮，防止重复操作
        self.ui.generateReportButton.setEnabled(False)
        self.ui.generateReportButton.setText("正在生成...")
        
        self.report_thread.start()
    
    def _on_report_generated(self, filename):
        """处理报告生成完成信号"""
        # 恢复按钮状态
        self.ui.generateReportButton.setEnabled(True)
        self.ui.generateReportButton.setText("生成报告")
        
        # 显示成功消息
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("成功")
        msg.setText(f"报告已生成：\n{filename}")
        msg.exec()

    def _update_system_info(self, system_info):
        """更新系统信息显示"""
        # 更新CPU信息
        cpu_percent = system_info['cpu_percent']
        self.ui.cpuProgressBar.setValue(int(cpu_percent))
        self.ui.cpuPercentLabel.setText(f"{cpu_percent:.1f}%")
        
        # 更新内存信息
        memory_percent = system_info['memory_percent']
        self.ui.memoryProgressBar.setValue(int(memory_percent))
        self.ui.memoryPercentLabel.setText(f"{memory_percent:.1f}%")
        
        # 保存系统信息用于生成报告
        self.system_data.append(system_info)
        # 只保留最近100条记录
        if len(self.system_data) > 100:
            self.system_data.pop(0)
    
    def _update_alerts(self, alerts):
        """更新告警状态"""
        # 根据阈值设置进度条样式
        self.ui.cpuProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red; }" if alerts['cpu_alert'] else "QProgressBar::chunk { background-color: green; }"
        )
        self.ui.memoryProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red; }" if alerts['memory_alert'] else "QProgressBar::chunk { background-color: green; }"
        )
    
    def _update_smtp_settings(self):
        """更新SMTP服务器设置"""
        settings = {
            'smtp_server': self.ui.smtpServerLineEdit.text(),
            'smtp_port': self.ui.smtpPortSpinBox.value(),
            'smtp_username': self.ui.smtpUsernameLineEdit.text(),
            'smtp_password': self.ui.smtpPasswordLineEdit.text(),
            'use_tls': self.ui.useTlsCheckBox.isChecked(),
            'alert_interval': self.ui.alertIntervalSpinBox.value()
        }
        self.notification_manager.configure_smtp(settings)
        self.config_manager.set_notification_config(settings)
    
    def _add_recipient(self):
        """添加收件人"""
        email = self.ui.recipientLineEdit.text().strip()
        if email:
            self.notification_manager.add_recipient(email)
            self.ui.recipientsListWidget.addItem(email)
            self.ui.recipientLineEdit.clear()
            self.config_manager.add_recipient(email)
    
    def _remove_recipient(self):
        """移除收件人"""
        current_item = self.ui.recipientsListWidget.currentItem()
        if current_item:
            email = current_item.text()
            self.notification_manager.recipients.remove(email)
            self.ui.recipientsListWidget.takeItem(self.ui.recipientsListWidget.row(current_item))
            self.config_manager.remove_recipient(email)
    
    def _update_alerts(self, alerts):
        """更新告警状态"""
        # 根据阈值设置进度条样式
        self.ui.cpuProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red; }" if alerts['cpu_alert'] else "QProgressBar::chunk { background-color: green; }"
        )
        self.ui.memoryProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red; }" if alerts['memory_alert'] else "QProgressBar::chunk { background-color: green; }"
        )
        
        # 如果有告警，发送邮件通知
        if any(alerts.values()):
            system_info = {
                'cpu_percent': float(self.ui.cpuPercentLabel.text().strip('%')),
                'memory_percent': float(self.ui.memoryPercentLabel.text().strip('%'))
            }
            self.notification_manager.send_system_alert(system_info, alerts)
    
    def _update_cpu_threshold(self, value):
        """更新CPU阈值"""
        self.system_monitor.set_threshold('cpu_percent', float(value))
        self.config_manager.set_system_monitor_config(cpu_percent=float(value))
    
    def _update_memory_threshold(self, value):
        """更新内存阈值"""
        self.system_monitor.set_threshold('memory_percent', float(value))
        self.config_manager.set_system_monitor_config(memory_percent=float(value))
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止监控线程
        self.monitor_thread.stop()
        self.monitor_thread.wait()
        self.file_manager_thread.stop()
        self.file_manager_thread.wait()
        super().closeEvent(event)