# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.systemMonitorTab = QWidget()
        self.systemMonitorTab.setObjectName(u"systemMonitorTab")
        self.verticalLayout_2 = QVBoxLayout(self.systemMonitorTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cpuGroupBox = QGroupBox(self.systemMonitorTab)
        self.cpuGroupBox.setObjectName(u"cpuGroupBox")
        self.verticalLayout_3 = QVBoxLayout(self.cpuGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cpuProgressBar = QProgressBar(self.cpuGroupBox)
        self.cpuProgressBar.setObjectName(u"cpuProgressBar")
        self.cpuProgressBar.setValue(0)

        self.horizontalLayout.addWidget(self.cpuProgressBar)

        self.cpuPercentLabel = QLabel(self.cpuGroupBox)
        self.cpuPercentLabel.setObjectName(u"cpuPercentLabel")

        self.horizontalLayout.addWidget(self.cpuPercentLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.cpuGroupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.cpuThresholdSpinBox = QSpinBox(self.cpuGroupBox)
        self.cpuThresholdSpinBox.setObjectName(u"cpuThresholdSpinBox")
        self.cpuThresholdSpinBox.setMaximum(100)
        self.cpuThresholdSpinBox.setValue(80)

        self.horizontalLayout_2.addWidget(self.cpuThresholdSpinBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.cpuGroupBox)

        self.memoryGroupBox = QGroupBox(self.systemMonitorTab)
        self.memoryGroupBox.setObjectName(u"memoryGroupBox")
        self.verticalLayout_4 = QVBoxLayout(self.memoryGroupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.memoryProgressBar = QProgressBar(self.memoryGroupBox)
        self.memoryProgressBar.setObjectName(u"memoryProgressBar")
        self.memoryProgressBar.setValue(0)

        self.horizontalLayout_3.addWidget(self.memoryProgressBar)

        self.memoryPercentLabel = QLabel(self.memoryGroupBox)
        self.memoryPercentLabel.setObjectName(u"memoryPercentLabel")

        self.horizontalLayout_3.addWidget(self.memoryPercentLabel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.memoryGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.memoryThresholdSpinBox = QSpinBox(self.memoryGroupBox)
        self.memoryThresholdSpinBox.setObjectName(u"memoryThresholdSpinBox")
        self.memoryThresholdSpinBox.setMaximum(100)
        self.memoryThresholdSpinBox.setValue(80)

        self.horizontalLayout_4.addWidget(self.memoryThresholdSpinBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.memoryGroupBox)

        self.tabWidget.addTab(self.systemMonitorTab, "")
        self.fileManagerTab = QWidget()
        self.fileManagerTab.setObjectName(u"fileManagerTab")
        self.verticalLayout_5 = QVBoxLayout(self.fileManagerTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tempDirGroupBox = QGroupBox(self.fileManagerTab)
        self.tempDirGroupBox.setObjectName(u"tempDirGroupBox")
        self.verticalLayout_6 = QVBoxLayout(self.tempDirGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.tempDirListWidget = QListWidget(self.tempDirGroupBox)
        self.tempDirListWidget.setObjectName(u"tempDirListWidget")

        self.horizontalLayout_5.addWidget(self.tempDirListWidget)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.addTempDirButton = QPushButton(self.tempDirGroupBox)
        self.addTempDirButton.setObjectName(u"addTempDirButton")

        self.verticalLayout_7.addWidget(self.addTempDirButton)

        self.removeTempDirButton = QPushButton(self.tempDirGroupBox)
        self.removeTempDirButton.setObjectName(u"removeTempDirButton")

        self.verticalLayout_7.addWidget(self.removeTempDirButton)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout_5.addWidget(self.tempDirGroupBox)

        self.cleanupGroupBox = QGroupBox(self.fileManagerTab)
        self.cleanupGroupBox.setObjectName(u"cleanupGroupBox")
        self.verticalLayout_8 = QVBoxLayout(self.cleanupGroupBox)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.cleanupGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.fileAgeThresholdSpinBox = QSpinBox(self.cleanupGroupBox)
        self.fileAgeThresholdSpinBox.setObjectName(u"fileAgeThresholdSpinBox")
        self.fileAgeThresholdSpinBox.setMinimum(0)
        self.fileAgeThresholdSpinBox.setMaximum(365)
        self.fileAgeThresholdSpinBox.setValue(7)

        self.horizontalLayout_6.addWidget(self.fileAgeThresholdSpinBox)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.scanFilesButton = QPushButton(self.cleanupGroupBox)
        self.scanFilesButton.setObjectName(u"scanFilesButton")

        self.verticalLayout_8.addWidget(self.scanFilesButton)

        self.scanResultTextEdit = QTextEdit(self.cleanupGroupBox)
        self.scanResultTextEdit.setObjectName(u"scanResultTextEdit")
        self.scanResultTextEdit.setReadOnly(True)

        self.verticalLayout_8.addWidget(self.scanResultTextEdit)

        self.cleanFilesButton = QPushButton(self.cleanupGroupBox)
        self.cleanFilesButton.setObjectName(u"cleanFilesButton")

        self.verticalLayout_8.addWidget(self.cleanFilesButton)


        self.verticalLayout_5.addWidget(self.cleanupGroupBox)

        self.tabWidget.addTab(self.fileManagerTab, "")
        self.notificationTab = QWidget()
        self.notificationTab.setObjectName(u"notificationTab")
        self.verticalLayout_9 = QVBoxLayout(self.notificationTab)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.smtpGroupBox = QGroupBox(self.notificationTab)
        self.smtpGroupBox.setObjectName(u"smtpGroupBox")
        self.verticalLayout_10 = QVBoxLayout(self.smtpGroupBox)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.smtpGroupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.smtpServerLineEdit = QLineEdit(self.smtpGroupBox)
        self.smtpServerLineEdit.setObjectName(u"smtpServerLineEdit")

        self.horizontalLayout_7.addWidget(self.smtpServerLineEdit)


        self.verticalLayout_10.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(self.smtpGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_8.addWidget(self.label_5)

        self.smtpPortSpinBox = QSpinBox(self.smtpGroupBox)
        self.smtpPortSpinBox.setObjectName(u"smtpPortSpinBox")
        self.smtpPortSpinBox.setMaximum(65535)
        self.smtpPortSpinBox.setValue(587)

        self.horizontalLayout_8.addWidget(self.smtpPortSpinBox)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_6 = QLabel(self.smtpGroupBox)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_9.addWidget(self.label_6)

        self.smtpUsernameLineEdit = QLineEdit(self.smtpGroupBox)
        self.smtpUsernameLineEdit.setObjectName(u"smtpUsernameLineEdit")

        self.horizontalLayout_9.addWidget(self.smtpUsernameLineEdit)


        self.verticalLayout_10.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_7 = QLabel(self.smtpGroupBox)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_10.addWidget(self.label_7)

        self.smtpPasswordLineEdit = QLineEdit(self.smtpGroupBox)
        self.smtpPasswordLineEdit.setObjectName(u"smtpPasswordLineEdit")
        self.smtpPasswordLineEdit.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_10.addWidget(self.smtpPasswordLineEdit)


        self.verticalLayout_10.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.useTlsCheckBox = QCheckBox(self.smtpGroupBox)
        self.useTlsCheckBox.setObjectName(u"useTlsCheckBox")
        self.useTlsCheckBox.setChecked(True)

        self.horizontalLayout_12.addWidget(self.useTlsCheckBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer)

        self.label_8 = QLabel(self.smtpGroupBox)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_12.addWidget(self.label_8)

        self.alertIntervalSpinBox = QSpinBox(self.smtpGroupBox)
        self.alertIntervalSpinBox.setObjectName(u"alertIntervalSpinBox")
        self.alertIntervalSpinBox.setMinimum(1)
        self.alertIntervalSpinBox.setMaximum(1440)
        self.alertIntervalSpinBox.setValue(10)

        self.horizontalLayout_12.addWidget(self.alertIntervalSpinBox)


        self.verticalLayout_10.addLayout(self.horizontalLayout_12)


        self.verticalLayout_9.addWidget(self.smtpGroupBox)

        self.recipientsGroupBox = QGroupBox(self.notificationTab)
        self.recipientsGroupBox.setObjectName(u"recipientsGroupBox")
        self.verticalLayout_11 = QVBoxLayout(self.recipientsGroupBox)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.recipientLineEdit = QLineEdit(self.recipientsGroupBox)
        self.recipientLineEdit.setObjectName(u"recipientLineEdit")

        self.horizontalLayout_11.addWidget(self.recipientLineEdit)

        self.addRecipientButton = QPushButton(self.recipientsGroupBox)
        self.addRecipientButton.setObjectName(u"addRecipientButton")

        self.horizontalLayout_11.addWidget(self.addRecipientButton)


        self.verticalLayout_11.addLayout(self.horizontalLayout_11)

        self.recipientsListWidget = QListWidget(self.recipientsGroupBox)
        self.recipientsListWidget.setObjectName(u"recipientsListWidget")

        self.verticalLayout_11.addWidget(self.recipientsListWidget)

        self.removeRecipientButton = QPushButton(self.recipientsGroupBox)
        self.removeRecipientButton.setObjectName(u"removeRecipientButton")

        self.verticalLayout_11.addWidget(self.removeRecipientButton)


        self.verticalLayout_9.addWidget(self.recipientsGroupBox)

        self.tabWidget.addTab(self.notificationTab, "")
        self.reportTab = QWidget()
        self.reportTab.setObjectName(u"reportTab")
        self.tabWidget.addTab(self.reportTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u76d1\u63a7\u4e0e\u81ea\u52a8\u5316\u5de5\u5177", None))
        self.cpuGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"CPU\u76d1\u63a7", None))
        self.cpuPercentLabel.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"CPU\u4f7f\u7528\u7387\u9608\u503c\uff1a", None))
        self.cpuThresholdSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u"%", None))
        self.memoryGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5185\u5b58\u76d1\u63a7", None))
        self.memoryPercentLabel.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5185\u5b58\u4f7f\u7528\u7387\u9608\u503c\uff1a", None))
        self.memoryThresholdSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u"%", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.systemMonitorTab), QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u76d1\u63a7", None))
        self.tempDirGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u4e34\u65f6\u76ee\u5f55\u7ba1\u7406", None))
        self.addTempDirButton.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u76ee\u5f55", None))
        self.removeTempDirButton.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u9664\u76ee\u5f55", None))
        self.cleanupGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u6e05\u7406", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7406\u9608\u503c\uff08\u5929\uff09\uff1a", None))
        self.scanFilesButton.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u6587\u4ef6", None))
        self.cleanFilesButton.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7406\u6587\u4ef6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fileManagerTab), QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u7ba1\u7406", None))
        self.smtpGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"SMTP\u670d\u52a1\u5668\u8bbe\u7f6e", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u670d\u52a1\u5668\u5730\u5740\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u7aef\u53e3\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\uff1a", None))
        self.useTlsCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528TLS\u52a0\u5bc6", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u544a\u8b66\u65f6\u95f4\u95f4\u9694\uff08\u5206\u949f\uff09\uff1a", None))
        self.recipientsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6536\u4ef6\u4eba\u7ba1\u7406", None))
        self.recipientLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6536\u4ef6\u4eba\u90ae\u7bb1\u5730\u5740", None))
        self.addRecipientButton.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0", None))
        self.removeRecipientButton.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u9664\u9009\u4e2d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.notificationTab), QCoreApplication.translate("MainWindow", u"\u901a\u77e5\u8bbe\u7f6e", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.reportTab), QCoreApplication.translate("MainWindow", u"\u62a5\u544a\u751f\u6210", None))
    # retranslateUi

