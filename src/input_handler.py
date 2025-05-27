class InputHandler:
    def __init__(self):
        self.required_fields = {
            'user_info': ['household_type', 'person_1_income'],
            'investment_goal': ['investment_horizon'],
            'property_info': ['purchase_price', 'down_payment', 'mortgage_rate', 'amortization'],
            'investment_info': ['appreciation_rate', 'rental_income', 'vacancy_rate', 'expense_rate']
        }
    
    def validate_input(self, data):
        """验证输入数据的完整性和有效性"""
        try:
            # 检查所有必需字段
            for category, fields in self.required_fields.items():
                if category not in data:
                    return False, f"Missing category: {category}"
                for field in fields:
                    if field not in data[category]:
                        return False, f"Missing field: {field} in {category}"
            # Dual-income 必须有 person_2_income
            if data['user_info'].get('household_type') == 'Dual-income' and 'person_2_income' not in data['user_info']:
                return False, "Missing field: person_2_income in user_info for Dual-income household"
            # 验证数值的合理性
            if data['property_info']['purchase_price'] <= 0:
                return False, "Purchase price must be greater than 0"
            if data['property_info']['down_payment'] >= data['property_info']['purchase_price']:
                return False, "Down payment must be less than purchase price"
            if not (0 <= data['investment_info']['appreciation_rate'] <= 20):
                return False, "Appreciation rate must be between 0 and 20%"
            if not (0 <= data['investment_info']['vacancy_rate'] <= 100):
                return False, "Vacancy rate must be between 0 and 100%"
            return True, "Input validation successful"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def process_input(self, data):
        """处理输入数据，转换为标准格式"""
        try:
            # 转换百分比为小数
            data['property_info']['mortgage_rate'] /= 100
            data['investment_info']['appreciation_rate'] /= 100
            data['investment_info']['vacancy_rate'] /= 100
            data['investment_info']['expense_rate'] /= 100
            
            # 计算贷款金额
            data['property_info']['loan_amount'] = (
                data['property_info']['purchase_price'] - 
                data['property_info']['down_payment']
            )
            
            return True, data
            
        except Exception as e:
            return False, f"Processing error: {str(e)}"
    
    def save_input(self, data, user_id=None):
        """保存输入数据到数据库"""
        # TODO: 实现数据库保存逻辑
        pass
    
    def load_input(self, scenario_id):
        """从数据库加载输入数据"""
        # TODO: 实现数据库加载逻辑
        pass 