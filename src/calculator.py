import numpy as np
import pandas as pd
import numpy_financial as npf
from datetime import datetime
from collections import defaultdict

class InvestmentCalculator:
    def __init__(self):
        self.monthly_periods = 12
        self.yearly_periods = 1
    
    def calculate_mortgage(self, principal, rate, years, start_period=1):
        """计算月供和还款计划，支持指定起始期数（用于 refinance）"""
        monthly_rate = rate / self.monthly_periods
        num_payments = years * self.monthly_periods
        if monthly_rate == 0:
            monthly_payment = principal / num_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        schedule = []
        balance = principal
        for period in range(num_payments):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            balance = max(0, balance - principal_payment)
            schedule.append({
                'period': start_period + period,
                'payment': monthly_payment,
                'principal': principal_payment,
                'interest': interest_payment,
                'balance': balance
            })
        return monthly_payment, pd.DataFrame(schedule)
    
    def calculate_property_value(self, purchase_price, appreciation_rate, years):
        """计算房产价值增长"""
        values = []
        current_value = purchase_price
        
        for year in range(years + 1):
            values.append({
                'year': year,
                'value': current_value
            })
            current_value *= (1 + appreciation_rate)
        
        return pd.DataFrame(values)
    
    def calculate_cash_flow(self, rental_income, expenses, mortgage_payment, vacancy_rate, tax_rate=0.0, deductible_interest=0.0):
        """计算现金流"""
        # 考虑空置率
        effective_rental_income = rental_income * (1 - vacancy_rate)
        
        # 计算净现金流
        net_cash_flow = effective_rental_income - expenses - mortgage_payment
        
        # 税后现金流（假设利息可抵税）
        taxable_income = effective_rental_income - expenses - deductible_interest
        tax = max(0, taxable_income) * tax_rate
        tax_adjusted_cash_flow = net_cash_flow - tax
        
        return net_cash_flow, tax_adjusted_cash_flow
    
    def calculate_roi(self, total_investment, total_return):
        """计算投资回报率"""
        return (total_return - total_investment) / total_investment if total_investment else 0
    
    def calculate_cash_on_cash(self, annual_cash_flow, total_investment):
        """计算现金回报率"""
        return annual_cash_flow / total_investment if total_investment else 0
    
    def calculate_irr(self, cash_flows):
        try:
            return npf.irr(cash_flows)
        except Exception as e:
            print(f"Error calculating IRR: {e}")
            return 0.0
    
    def calculate_refinance_schedule(self, principal, rate, years, refinance_years, custom_amounts=None, start_period=1):
        """
        支持多次 refinance，返回完整摊销表和 refinance 事件列表。
        refinance_years: [5, 10, ...]
        custom_amounts: {5: 200000, 10: 180000, ...}  # 可选，指定每次 refinance 金额
        """
        refinance_years = sorted(refinance_years)
        schedule = []
        refinance_events = []
        current_principal = principal
        current_rate = rate
        current_years = years
        current_start_period = start_period
        total_periods = years * self.monthly_periods
        periods_done = 0
        for idx, ref_year in enumerate(refinance_years):
            months_until_ref = (ref_year - (periods_done // 12)) * self.monthly_periods
            # 只算到 refinance 年份
            months_this_leg = min(months_until_ref, current_years * self.monthly_periods)
            monthly_payment, df = self.calculate_mortgage(current_principal, current_rate, current_years, start_period=current_start_period)
            df_leg = df.iloc[:months_this_leg].copy()
            schedule.append(df_leg)
            # refinance 时点余额
            ref_balance = df_leg.iloc[-1]['balance']
            # 新贷款金额
            if custom_amounts and ref_year in custom_amounts:
                new_loan = custom_amounts[ref_year]
            else:
                new_loan = ref_balance
            cash_out = max(0, new_loan - ref_balance)
            refinance_events.append({
                'year': ref_year,
                'old_balance': ref_balance,
                'new_loan': new_loan,
                'cash_out': cash_out,
                'monthly_payment': None  # 后面补充
            })
            # 更新参数
            current_principal = new_loan
            current_start_period = df_leg['period'].iloc[-1] + 1
            current_years = years - ref_year
            periods_done += months_this_leg
        # 最后一段
        if current_years > 0:
            monthly_payment, df = self.calculate_mortgage(current_principal, current_rate, current_years, start_period=current_start_period)
            schedule.append(df)
        # 合并所有分段
        full_schedule = pd.concat(schedule, ignore_index=True)
        # 补充每次 refinance 后的月供
        for event in refinance_events:
            mp, _ = self.calculate_mortgage(event['new_loan'], current_rate, current_years)
            event['monthly_payment'] = mp
        return full_schedule, refinance_events
    
    def calculate_all(self, input_data):
        """计算所有投资指标"""
        # 合并两个人的收入
        user_info = input_data.get('user_info', {})
        if user_info.get('household_type') == 'Dual-income':
            income = user_info.get('person_1_income', 0) + user_info.get('person_2_income', 0)
        else:
            income = user_info.get('person_1_income', 0)
        # 兼容新结构：从资产列表中取第一个资产
        assets = input_data.get('assets', [])
        if assets and isinstance(assets, list):
            asset = assets[0]
            current_asset_id = 0  # 默认用第一个资产，property_id=0
        else:
            asset = input_data.get('property_info', {})
            current_asset_id = 0
        # 兼容老结构
        property_info = asset if 'purchase_price' in asset else input_data.get('property_info', {})
        investment_info = asset if 'appreciation_rate' in asset else input_data.get('investment_info', {})
        years = input_data.get('investment_goal', {}).get('investment_horizon', 30)
        refinance_info = input_data.get('refinance_info', {})
        refinance_years = refinance_info.get('refinance_years', [])
        custom_amounts = refinance_info.get('custom_amounts', None)
        # 新增税务参数
        tax_rate = investment_info.get('tax_rate', 0.25)
        depreciation_years = investment_info.get('depreciation_years', 27.5)
        building_ratio = investment_info.get('building_ratio', 0.8)
        property_tax_rate = investment_info.get('property_tax_rate', 0.012)
        insurance_sim = investment_info.get('insurance', 0)
        maintenance_sim = investment_info.get('maintenance', 0)
        management_fee_sim = investment_info.get('management_fee', 0)
        capital_gains_tax_rate = investment_info.get('capital_gains_tax_rate', 0.2)
        
        # 贷款金额
        principal = property_info.get('loan_amount', 0)
        rate = property_info.get('mortgage_rate', 0)
        amortization = property_info.get('amortization', 30)
        purchase_price = property_info.get('purchase_price', 0)
        down_payment = property_info.get('down_payment', 0)
        appreciation_rate = investment_info.get('appreciation_rate', 0)
        rental_income = investment_info.get('rental_income', 0)
        vacancy_rate = investment_info.get('vacancy_rate', 0)
        expense_rate = investment_info.get('expense_rate', 0)
        annual_expenses_sim = purchase_price * expense_rate

        # 处理 expenses
        expenses = input_data.get('expenses', [])
        # 以 property_id 关联当前资产（默认用第一个资产，property_id=0）
        expense_by_year_type = defaultdict(lambda: defaultdict(float))
        for exp in expenses:
            # property_id 兼容字符串和索引
            if str(exp.get('property_id', '0')).endswith(str(current_asset_id)):
                year = pd.to_datetime(exp['date']).year
                expense_by_year_type[year][exp['expense_type']] += exp['amount']

        # 贷款摊销表和 refinance
        if refinance_years:
            mortgage_schedule, refinance_events = self.calculate_refinance_schedule(
                principal, rate, amortization, refinance_years, custom_amounts
            )
        else:
            monthly_payment, mortgage_schedule = self.calculate_mortgage(principal, rate, amortization)
            refinance_events = []
        
        # 房产价值增长
        property_values = self.calculate_property_value(
            property_info.get('purchase_price', 0),
            investment_info.get('appreciation_rate', 0),
            years
        )
        
        # 现金流等参数初始化
        monthly_payment = mortgage_schedule.iloc[0]['payment'] if not mortgage_schedule.empty else 0
        mortgage_schedule['year'] = (mortgage_schedule['period'] - 1) // 12
        annual_interest = mortgage_schedule.groupby('year')['interest'].sum().to_dict()
        year_end_balances = mortgage_schedule.groupby(mortgage_schedule['year'])['balance'].last().to_dict()

        # 折旧
        building_value = purchase_price * building_ratio
        annual_depreciation = building_value / depreciation_years if depreciation_years > 0 else 0
        # 年度税务明细
        annual_tax_results = []
        annual_expense_details = []
        start_year = datetime.now().year
        for year_idx in range(years):
            year = start_year + year_idx
            # 优先用 expenses 里的真实支出
            year_exp = expense_by_year_type.get(year, {})
            property_tax = year_exp.get('Property Tax', purchase_price * property_tax_rate)
            insurance = year_exp.get('Home Insurance', insurance_sim)
            maintenance = year_exp.get('Maintenance', maintenance_sim)
            management_fee = year_exp.get('Management Fee', management_fee_sim)
            interest = year_exp.get('Interest', annual_interest.get(year_idx, 0))
            depreciable = year_exp.get('Depreciable', 0)
            other = year_exp.get('Other', 0)
            # 运营费用合计
            annual_operating_expenses = annual_expenses_sim + property_tax + insurance + maintenance + management_fee + other
            # 可抵税支出合计
            total_depreciation = annual_depreciation + depreciable
            # 年度租金
            gross_rent = rental_income * 12 * (1 - vacancy_rate)
            # 应税收入
            taxable_income = gross_rent - annual_operating_expenses - interest - total_depreciation
            income_tax = max(0, taxable_income) * tax_rate
            # 税前现金流
            net_cash = gross_rent - annual_operating_expenses - mortgage_schedule[mortgage_schedule['year']==year_idx]['payment'].sum()
            # 税后现金流
            after_tax_cash_flow = net_cash - income_tax
            annual_tax_results.append({
                'year': year,
                'gross_rent': gross_rent,
                'interest': interest,
                'operating_expenses': annual_operating_expenses,
                'depreciation': total_depreciation,
                'taxable_income': taxable_income,
                'income_tax': income_tax,
                'net_cash_flow': net_cash,
                'after_tax_cash_flow': after_tax_cash_flow
            })
            annual_expense_details.append({
                'year': year,
                'property_tax': property_tax,
                'insurance': insurance,
                'maintenance': maintenance,
                'management_fee': management_fee,
                'interest': interest,
                'depreciable': depreciable,
                'other': other
            })
        # 资本利得税
        total_value = property_values.iloc[-1]['value'] if not property_values.empty else 0
        total_depreciation_sum = (annual_depreciation + sum([expense_by_year_type[y].get('Depreciable', 0) for y in range(start_year, start_year+years)]))
        capital_gain = total_value - purchase_price
        taxable_gain = capital_gain - total_depreciation_sum
        capital_gains_tax = max(0, taxable_gain) * capital_gains_tax_rate
        # 总回报
        total_investment = down_payment
        total_equity = total_value - mortgage_schedule.iloc[-1]['balance'] if not mortgage_schedule.empty else 0
        roi = self.calculate_roi(total_investment, total_equity) if total_investment else 0
        cash_on_cash = self.calculate_cash_on_cash(annual_tax_results[0]['net_cash_flow'] if annual_tax_results else 0, total_investment) if total_investment else 0
        leverage_roi = (total_equity + sum([e['cash_out'] for e in refinance_events])) / (down_payment or 1)
        # 优化税后 ROI：考虑税后现金流和资本利得税
        total_after_tax_cash_flow = sum([r['after_tax_cash_flow'] for r in annual_tax_results])
        tax_adjusted_roi = (total_equity + total_after_tax_cash_flow - capital_gains_tax - total_investment) / total_investment if total_investment else 0
        # IRR（用税后现金流）
        cash_flows = [-total_investment]
        for year_idx in range(years):
            year_cash_flow = annual_tax_results[year_idx]['after_tax_cash_flow']
            if year_idx == years - 1:
                year_cash_flow += total_value - capital_gains_tax
            cash_flows.append(year_cash_flow)
        irr = self.calculate_irr(cash_flows)
        
        # 年度总支出
        annual_total_expenses = []
        for detail in annual_expense_details:
            total = sum([v for k, v in detail.items() if k != 'year'])
            annual_total_expenses.append({'year': detail['year'], 'total_expense': total})
        # 按资产分组的支出汇总
        property_expense_summary = defaultdict(lambda: defaultdict(float))
        for exp in expenses:
            property_expense_summary[exp['property_id']][exp['expense_type']] += exp['amount']

        return {
            'total_value': total_value,
            'total_equity': total_equity,
            'monthly_cash_flow': annual_tax_results[0]['net_cash_flow'] / 12 if annual_tax_results else 0,
            'tax_adjusted_cash_flow': annual_tax_results[0]['after_tax_cash_flow'] / 12 if annual_tax_results else 0,
            'roi': roi,
            'leverage_roi': leverage_roi,
            'tax_adjusted_roi': tax_adjusted_roi,
            'cash_on_cash': cash_on_cash,
            'irr': irr,
            'mortgage_schedule': mortgage_schedule,
            'property_values': property_values,
            'refinance_events': refinance_events,
            'year_end_balances': year_end_balances,
            'annual_tax_results': annual_tax_results,
            'annual_expense_details': annual_expense_details,
            'annual_total_expenses': annual_total_expenses,
            'property_expense_summary': dict(property_expense_summary),
            'capital_gains_tax': capital_gains_tax
        } 