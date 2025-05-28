import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import (
    init_db, create_user, create_scenario, create_property,
    insert_expense, insert_income, create_mortgage,
    get_property_expenses, get_property_incomes, get_property_mortgages
)

def test_database():
    # 初始化数据库
    init_db()
    
    # 创建测试用户
    user_id = create_user("test@example.com", "Test User")
    print(f"Created user with ID: {user_id}")
    
    # 创建测试场景
    scenario_data = {
        "description": "Test scenario",
        "investment_horizon": 10
    }
    scenario_id = create_scenario(user_id, "Test Scenario", str(scenario_data))
    print(f"Created scenario with ID: {scenario_id}")
    
    # 创建测试房产
    property_data = {
        "property_type": "Residential",
        "purchase_price": 500000,
        "down_payment": 100000,
        "mortgage_rate": 0.05,
        "mortgage_term": 30,
        "rental_income": 2500,
        "expected_appreciation": 0.03,
        "vacancy_rate": 0.05
    }
    property_id = create_property(scenario_id, property_data)
    print(f"Created property with ID: {property_id}")
    
    # 添加测试支出
    expense_id = insert_expense(
        property_id,
        "Property Tax",
        "Tax",
        5000,
        "2024-01-01"
    )
    print(f"Created expense with ID: {expense_id}")
    
    # 添加测试收入
    income_id = insert_income(
        property_id,
        "Monthly Rent",
        "Rental",
        2500,
        "2024-01-01"
    )
    print(f"Created income with ID: {income_id}")
    
    # 添加测试贷款
    loan_data = {
        "loan_amount": 400000,
        "interest_rate": 0.05,
        "term_years": 30,
        "start_date": "2024-01-01",
        "end_date": "2054-01-01"
    }
    mortgage_id = create_mortgage(property_id, loan_data)
    print(f"Created mortgage with ID: {mortgage_id}")
    
    # 查询并显示数据
    print("\nProperty Expenses:")
    expenses = get_property_expenses(property_id)
    for expense in expenses:
        print(expense)
    
    print("\nProperty Incomes:")
    incomes = get_property_incomes(property_id)
    for income in incomes:
        print(income)
    
    print("\nProperty Mortgages:")
    mortgages = get_property_mortgages(property_id)
    for mortgage in mortgages:
        print(mortgage)

if __name__ == "__main__":
    test_database() 