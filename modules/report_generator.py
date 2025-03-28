from datetime import datetime
from typing import Dict, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from jinja2 import Environment, FileSystemLoader
import os


class ReportGenerator:
    def __init__(self):
        self.report_dir = 'reports'
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def generate_pdf_report(self, system_data: List[Dict[str, any]],
                           file_cleanup_data: Dict[str, int]) -> str:
        """生成PDF格式的系统健康报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.report_dir, f'system_report_{timestamp}.pdf')

        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        # 注册微软雅黑字体
        pdfmetrics.registerFont(TTFont('Microsoft YaHei', 'msyh.ttc'))  # 使用Windows系统自带的微软雅黑字体

        # 使用默认样式，并修改字体
        styles['Heading1'].fontName = 'Microsoft YaHei'
        styles['Heading1'].fontSize = 18
        styles['Heading1'].textColor = colors.black
        styles['Heading1'].alignment = 1
        
        styles['Heading2'].fontName = 'Microsoft YaHei'
        styles['Heading2'].fontSize = 14
        styles['Heading2'].textColor = colors.black
        styles['Heading2'].alignment = 1

        styles['Normal'].fontName = 'Microsoft YaHei'
        styles['Normal'].fontSize = 12
        styles['Normal'].textColor = colors.black


        story = []

        # 添加标题
        story.append(Paragraph('系统健康报告', styles['Heading1']))
        story.append(Spacer(1, 12))

        # 添加系统数据部分
        self._add_system_data_section(story, system_data, styles)

        # 添加文件清理数据部分
        self._add_cleanup_data_section(story, file_cleanup_data, styles)

        doc.build(story)
        return filename

    def generate_html_report(self, system_data: List[Dict[str, any]],
                            file_cleanup_data: Dict[str, int]) -> str:
        """生成HTML格式的系统健康报告"""
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report_template.html')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.report_dir, f'system_report_{timestamp}.html')
        
        html_content = template.render(
            system_data=system_data,
            file_cleanup_data=file_cleanup_data,
            generated_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    def _add_system_data_section(self, story: List, data: List[Dict[str, any]],
                                styles: Dict) -> None:
        """添加系统监控数据到PDF报告"""
        story.append(Paragraph('系统资源使用情况', styles['Heading2']))
        story.append(Spacer(1, 12))
        
        table_data = [
            ['时间', 'CPU使用率', '内存使用率']
        ]
        for item in data:
            table_data.append([
                item['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                f"{item['cpu_percent']}%",
                f"{item['memory_percent']}%"
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Microsoft YaHei'),  # 表头使用微软雅黑
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Microsoft YaHei'),  # 表格内容使用微软雅黑
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
    
    def _add_cleanup_data_section(self, story: List, data: Dict[str, int],
                                 styles: Dict) -> None:
        """添加文件清理数据到PDF报告"""
        story.append(Spacer(1, 20))
        story.append(Paragraph('文件清理统计', styles['Heading2']))
        story.append(Spacer(1, 12))
        
        cleanup_text = f"清理文件数量: {data['files_cleaned']}\n"
        cleanup_text += f"清理空间大小: {data['bytes_cleaned'] / 1024 / 1024:.2f} MB"
        
        story.append(Paragraph(cleanup_text, styles['Normal']))
