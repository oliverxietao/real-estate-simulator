from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12
        )
        self.normal_style = self.styles['Normal']
    
    def generate_report(self, data):
        """生成投资报告"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # 添加标题
        story.append(Paragraph("Real Estate Investment Analysis Report", self.title_style))
        story.append(Spacer(1, 12))
        
        # 用户信息
        story.append(Paragraph("User Information", self.heading_style))
        user_info = data.get('user_info', {})
        user_data = [
            ["Annual Income", f"${user_info.get('income', 0):,.2f}"],
            ["Target Retirement Age", str(user_info.get('retirement_age', '--'))],
            ["Target Monthly Income", f"${user_info.get('target_income', 0):,.2f}"]
        ]
        story.append(self._create_table(user_data))
        story.append(Spacer(1, 12))
        
        # 投资目标
        story.append(Paragraph("Investment Goal", self.heading_style))
        investment_goal = data.get('investment_goal', {})
        goal_data = [
            ["Investment Horizon", f"{investment_goal.get('investment_horizon', '--')} years"]
        ]
        story.append(self._create_table(goal_data))
        story.append(Spacer(1, 12))
        
        # 房产信息
        story.append(Paragraph("Property Information", self.heading_style))
        property_info = data.get('property_info', {})
        property_data = [
            ["Purchase Price", f"${property_info['purchase_price']:,.2f}"],
            ["Down Payment", f"${property_info['down_payment']:,.2f}"],
            ["Loan Amount", f"${property_info['loan_amount']:,.2f}"],
            ["Mortgage Rate", f"{property_info['mortgage_rate']*100:.2f}%"],
            ["Amortization Period", f"{property_info['amortization']} years"]
        ]
        story.append(self._create_table(property_data))
        story.append(Spacer(1, 12))
        
        # 投资假设
        story.append(Paragraph("Investment Assumptions", self.heading_style))
        investment_info = data['investment_info']
        investment_data = [
            ["Expected Appreciation", f"{investment_info['appreciation_rate']*100:.2f}%"],
            ["Monthly Rental Income", f"${investment_info['rental_income']:,.2f}"],
            ["Vacancy Rate", f"{investment_info['vacancy_rate']*100:.2f}%"],
            ["Annual Expense Rate", f"{investment_info['expense_rate']*100:.2f}%"]
        ]
        story.append(self._create_table(investment_data))
        
        # 生成PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_table(self, data):
        """创建表格"""
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table 