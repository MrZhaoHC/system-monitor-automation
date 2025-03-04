from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread, Signal
from .ui_main_window import Ui_MainWindow
from modules.system_monitor import SystemMonitor

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
        
        # 初始化UI组件
        self._init_ui()
        
        # 创建并启动监控线程
        self.monitor_thread = SystemMonitorThread(self.system_monitor)
        self.monitor_thread.system_info_updated.connect(self.update_system_info)
        self.monitor_thread.alerts_updated.connect(self.update_alerts)
        self.monitor_thread.start()
    
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
        super().closeEvent(event)