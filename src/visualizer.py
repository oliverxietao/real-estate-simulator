import plotly.graph_objects as go
import plotly.express as px

class DataVisualizer:
    def __init__(self):
        self.chart_types = {
            'property_value': 'line',
            'cash_flow': 'bar',
            'roi_comparison': 'scatter'
        }
    
    def create_property_value_chart(self, property_values):
        """创建房产价值趋势图"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=property_values['year'],
            y=property_values['value'],
            mode='lines+markers',
            name='Property Value',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig.update_layout(
            title='Property Value Growth Over Time',
            xaxis_title='Year',
            yaxis_title='Value ($)',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
    
    def create_mortgage_schedule_chart(self, mortgage_schedule):
        """创建贷款还款计划图"""
        fig = go.Figure()
        
        # 添加本金和利息的堆叠柱状图
        fig.add_trace(go.Bar(
            x=mortgage_schedule['period'],
            y=mortgage_schedule['principal'],
            name='Principal',
            marker_color='#2ca02c'
        ))
        
        fig.add_trace(go.Bar(
            x=mortgage_schedule['period'],
            y=mortgage_schedule['interest'],
            name='Interest',
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            title='Mortgage Payment Schedule',
            xaxis_title='Payment Period',
            yaxis_title='Amount ($)',
            barmode='stack',
            template='plotly_white'
        )
        
        return fig
    
    def create_cash_flow_chart(self, monthly_cash_flow, years):
        """创建现金流图"""
        # 生成月度数据
        months = range(1, years * 12 + 1)
        cash_flows = [monthly_cash_flow] * len(months)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=months,
            y=cash_flows,
            name='Monthly Cash Flow',
            marker_color='#17becf'
        ))
        
        fig.update_layout(
            title='Monthly Cash Flow Projection',
            xaxis_title='Month',
            yaxis_title='Cash Flow ($)',
            template='plotly_white'
        )
        
        return fig
    
    def create_roi_comparison_chart(self, results):
        """创建回报率对比图"""
        metrics = ['ROI', 'Cash on Cash', 'IRR']
        values = [results['roi'], results['cash_on_cash'], results['irr']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=metrics,
            y=values,
            text=[f'{v:.1%}' for v in values],
            textposition='auto',
            marker_color='#9467bd'
        ))
        
        fig.update_layout(
            title='Return Metrics Comparison',
            xaxis_title='Metric',
            yaxis_title='Return Rate',
            template='plotly_white'
        )
        
        return fig
    
    def create_all_charts(self, results):
        """创建所有图表"""
        charts = []
        
        # 添加房产价值趋势图
        charts.append(self.create_property_value_chart(results['property_values']))
        
        # 添加贷款还款计划图
        charts.append(self.create_mortgage_schedule_chart(results['mortgage_schedule']))
        
        # 添加现金流图
        charts.append(self.create_cash_flow_chart(
            results['monthly_cash_flow'],
            len(results['property_values']) - 1
        ))
        
        # 添加回报率对比图
        charts.append(self.create_roi_comparison_chart(results))
        
        return charts

    def create_equity_vs_balance_chart(self, property_values, mortgage_schedule):
        """年度房产价值、贷款余额、equity 曲线图"""
        # 按年聚合贷款余额
        mortgage_schedule['year'] = (mortgage_schedule['period'] - 1) // 12
        year_balance = mortgage_schedule.groupby('year')['balance'].last().reset_index()
        df = property_values.copy()
        df = df.merge(year_balance, left_on='year', right_on='year', how='left')
        df['balance'] = df['balance'].fillna(method='ffill').fillna(0)
        df['equity'] = df['value'] - df['balance']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['year'], y=df['value'], name='Property Value', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df['year'], y=df['balance'], name='Loan Balance', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df['year'], y=df['equity'], name='Equity', line=dict(color='green')))
        fig.update_layout(title='Equity & Loan Balance Over Time', xaxis_title='Year', yaxis_title='Amount ($)', template='plotly_white')
        return fig

    def create_strategy_comparison_chart(self, results_list, labels):
        """多策略 ROI/杠杆/税后ROI/IRR 对比图"""
        metrics = ['roi', 'leverage_roi', 'tax_adjusted_roi', 'irr']
        metric_names = ['ROI', 'Leverage ROI', 'Tax-Adjusted ROI', 'IRR']
        data = {label: [r.get(m, 0) for m in metrics] for label, r in zip(labels, results_list)}
        fig = go.Figure()
        for idx, label in enumerate(labels):
            fig.add_trace(go.Bar(x=metric_names, y=data[label], name=label))
        fig.update_layout(barmode='group', title='Strategy Comparison', yaxis_title='Return Rate', template='plotly_white')
        return fig 