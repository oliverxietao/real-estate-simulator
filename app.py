import streamlit as st
from src.input_handler import InputHandler
from src.calculator import InvestmentCalculator
from src.visualizer import DataVisualizer
from src.report_generator import ReportGenerator
import json
from datetime import datetime, timedelta
from src.db import (
    init_db, create_user, create_scenario, create_property,
    create_expense, create_income, create_mortgage,
    get_property_expenses, get_property_incomes, get_property_mortgages,
    get_scenario_properties
)

# Initialize database
init_db()

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'property_data' not in st.session_state:
    st.session_state.property_data = []

def main():
    st.set_page_config(page_title="Real Estate Investment Simulator", layout="wide")
    
    # Sidebar navigation with all steps
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Step 1: Household & Income",
            "Step 2: Investment Goal",
            "Step 3: First Property Planning",
            "Step 4: Rent & Growth",
            "Step 5: Other Financial Info",
            "Step 6: Refinance Strategy",
            "Data"
        ]
    )
    
    if page == "Step 1: Household & Income":
        show_household_income_page()
    elif page == "Step 2: Investment Goal":
        show_investment_goal_page()
    elif page == "Step 3: First Property Planning":
        show_property_planning_page()
    elif page == "Step 4: Rent & Growth":
        show_rent_growth_page()
    elif page == "Step 5: Other Financial Info":
        show_financial_info_page()
    elif page == "Step 6: Refinance Strategy":
        show_refinance_strategy_page()
    else:
        show_data_page()

def show_input_page(input_handler, calculator):
    # Questions and their corresponding input types
    questions = [
        # Step 1: User Profile & Income
        {
            "id": "household_type",
            "question": "👤 What is your household structure?",
            "subtitle": "This helps us understand your income situation.",
            "type": "radio",
            "options": ["Single-income", "Dual-income"],
            "category": "user_info"
        },
        {
            "id": "person_1_income",
            "question": "💰 What is your annual income (Person 1)?",
            "subtitle": "Enter your yearly income before taxes.",
            "type": "number",
            "min": 0,
            "step": 10000,
            "category": "user_info"
        },
        {
            "id": "person_2_income",
            "question": "💰 What is your annual income (Person 2)?",
            "subtitle": "Enter your partner's yearly income before taxes.",
            "type": "number",
            "min": 0,
            "step": 10000,
            "category": "user_info",
            "condition": lambda data: data.get('household_type') == "Dual-income"
        },
        
        # Step 2: Investment Goal
        {
            "id": "retirement_age",
            "question": "🎯 What age do you plan to retire?",
            "subtitle": "This helps us plan your investment timeline.",
            "type": "number",
            "min": 30,
            "max": 80,
            "value": 65,
            "category": "investment_goal"
        },
        {
            "id": "retirement_income",
            "question": "🪙 How much monthly passive income do you expect during retirement?",
            "subtitle": "Enter your target monthly passive income.",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "investment_goal"
        },
        {
            "id": "has_net_worth_target",
            "question": "💼 Do you have a net worth target?",
            "subtitle": "For example, $3,000,000 by age 60.",
            "type": "radio",
            "options": ["Yes", "No"],
            "category": "investment_goal"
        },
        {
            "id": "net_worth_target",
            "question": "What is your net worth target?",
            "subtitle": "Enter your target net worth amount.",
            "type": "number",
            "min": 0,
            "step": 100000,
            "category": "investment_goal",
            "condition": lambda data: data.get('has_net_worth_target') == "Yes"
        },
        
        # Step 3: First Property Planning
        {
            "id": "property_ownership",
            "question": "🏡 Do you currently own a home or plan to purchase one?",
            "subtitle": "This helps us understand your current situation.",
            "type": "radio",
            "options": ["Own", "Plan to buy"],
            "category": "property_info"
        },
        {
            "id": "property_type",
            "question": "📊 Is the first property a:",
            "subtitle": "This affects tax deductions and investment calculations.",
            "type": "radio",
            "options": ["Principal Residence", "Investment Property"],
            "category": "property_info"
        },
        {
            "id": "has_down_payment",
            "question": "💵 Do you already have a down payment saved?",
            "subtitle": "This is the initial cash investment for the property.",
            "type": "radio",
            "options": ["Yes", "No"],
            "category": "property_info"
        },
        {
            "id": "down_payment",
            "question": "How much is your down payment?",
            "subtitle": "Enter the amount you have saved for the down payment.",
            "type": "number",
            "min": 0,
            "step": 10000,
            "category": "property_info",
            "condition": lambda data: data.get('has_down_payment') == "Yes"
        },
        {
            "id": "yearly_savings",
            "question": "How much can you save yearly for the down payment?",
            "subtitle": "This helps us calculate how long until you can purchase.",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "property_info",
            "condition": lambda data: data.get('has_down_payment') == "No"
        },
        {
            "id": "savings_years",
            "question": "For how many years will you save?",
            "subtitle": "This is the timeframe for saving the down payment.",
            "type": "number",
            "min": 1,
            "max": 30,
            "category": "property_info",
            "condition": lambda data: data.get('has_down_payment') == "No"
        },
        {
            "id": "purchase_price",
            "question": "🏠 What is your budget or target price for the first property?",
            "subtitle": "Enter the expected purchase price of the property.",
            "type": "number",
            "min": 0,
            "step": 10000,
            "category": "property_info"
        },
        {
            "id": "closing_date",
            "question": "📅 What is the expected closing date?",
            "subtitle": "This is the expected purchase date.",
            "type": "date",
            "category": "property_info"
        },
        {
            "id": "same_mortgage_date",
            "question": "📆 Is the mortgage start date the same as the closing date?",
            "subtitle": "Choose whether to set a different mortgage start date.",
            "type": "checkbox",
            "category": "property_info"
        },
        {
            "id": "mortgage_start_date",
            "question": "When will your mortgage start?",
            "subtitle": "Enter the date when your mortgage payments will begin.",
            "type": "date",
            "category": "property_info",
            "condition": lambda data: data.get('same_mortgage_date') == False
        },
        {
            "id": "mortgage_rate",
            "question": "🏦 What is the expected mortgage interest rate?",
            "subtitle": "Enter the expected interest rate for your mortgage.",
            "type": "number",
            "min": 0.0,
            "max": 20.0,
            "value": 5.0,
            "step": 0.1,
            "category": "property_info"
        },
        {
            "id": "amortization",
            "question": "📈 What is the amortization period?",
            "subtitle": "This is the total time to pay off the mortgage.",
            "type": "selectbox",
            "options": [20, 25, 30],
            "category": "property_info"
        },
        {
            "id": "loan_term",
            "question": "⌛ What is the loan term (fixed rate period)?",
            "subtitle": "This is the fixed rate period for your mortgage.",
            "type": "selectbox",
            "options": [1, 2, 3, 4, 5],
            "category": "property_info"
        },
        
        # Step 4: Rent & Property Growth Assumptions
        {
            "id": "rent_input_type",
            "question": "💼 Will you input actual rent or use estimated rental yield?",
            "subtitle": "Choose between actual rent amount or rental yield percentage.",
            "type": "radio",
            "options": ["Input actual rent", "Use rental yield"],
            "category": "investment_info",
            "condition": lambda data: data.get('property_type') == "Investment Property"
        },
        {
            "id": "rental_income",
            "question": "What monthly rent do you expect?",
            "subtitle": "Enter the expected monthly rental income.",
            "type": "number",
            "min": 0,
            "step": 100,
            "category": "investment_info",
            "condition": lambda data: data.get('property_type') == "Investment Property" and data.get('rent_input_type') == "Input actual rent"
        },
        {
            "id": "rental_yield",
            "question": "What rental yield do you expect?",
            "subtitle": "Enter the expected annual rental yield as a percentage.",
            "type": "number",
            "min": 0.0,
            "max": 20.0,
            "step": 0.1,
            "category": "investment_info",
            "condition": lambda data: data.get('property_type') == "Investment Property" and data.get('rent_input_type') == "Use rental yield"
        },
        {
            "id": "appreciation_rate",
            "question": "📈 Expected annual property appreciation rate?",
            "subtitle": "Enter the expected annual property value increase.",
            "type": "slider",
            "min": 0.0,
            "max": 20.0,
            "value": 3.0,
            "step": 0.1,
            "category": "investment_info"
        },
        {
            "id": "vacancy_rate",
            "question": "📉 Expected vacancy rate?",
            "subtitle": "Enter the expected percentage of time the property will be vacant.",
            "type": "slider",
            "min": 0.0,
            "max": 100.0,
            "value": 5.0,
            "step": 0.1,
            "category": "investment_info",
            "condition": lambda data: data.get('property_type') == "Investment Property"
        },
        {
            "id": "expense_type",
            "question": "🧾 How would you like to input property expenses?",
            "subtitle": "Choose between percentage of property value or actual amount.",
            "type": "radio",
            "options": ["Percentage of property value", "Actual amount"],
            "category": "investment_info"
        },
        {
            "id": "expense_rate",
            "question": "What annual expense rate do you expect?",
            "subtitle": "Enter the expected annual expenses as a percentage of property value.",
            "type": "number",
            "min": 0.0,
            "max": 10.0,
            "value": 1.0,
            "step": 0.1,
            "category": "investment_info",
            "condition": lambda data: data.get('expense_type') == "Percentage of property value"
        },
        {
            "id": "annual_expenses",
            "question": "What annual expenses do you expect?",
            "subtitle": "Enter the expected annual property expenses.",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "investment_info",
            "condition": lambda data: data.get('expense_type') == "Actual amount"
        },
        
        # Step 5: Other Financial Information
        {
            "id": "has_investment_loan",
            "question": "💸 Do you have an investment loan?",
            "subtitle": "This helps us understand your current financial obligations.",
            "type": "checkbox",
            "category": "financial_info"
        },
        {
            "id": "investment_loan_amount",
            "question": "What is your investment loan amount?",
            "subtitle": "Enter the total amount of your investment loan.",
            "type": "number",
            "min": 0,
            "step": 10000,
            "category": "financial_info",
            "condition": lambda data: data.get('has_investment_loan') == True
        },
        {
            "id": "investment_loan_start_date",
            "question": "When did your investment loan start?",
            "subtitle": "Enter the start date of your investment loan.",
            "type": "date",
            "category": "financial_info",
            "condition": lambda data: data.get('has_investment_loan') == True
        },
        {
            "id": "investment_loan_rate",
            "question": "What is your investment loan interest rate?",
            "subtitle": "Enter the interest rate of your investment loan.",
            "type": "number",
            "min": 0.0,
            "max": 20.0,
            "step": 0.1,
            "category": "financial_info",
            "condition": lambda data: data.get('has_investment_loan') == True
        },
        {
            "id": "investment_loan_payment",
            "question": "What is your monthly investment loan payment?",
            "subtitle": "Enter your monthly payment for the investment loan.",
            "type": "number",
            "min": 0,
            "step": 100,
            "category": "financial_info",
            "condition": lambda data: data.get('has_investment_loan') == True
        },
        {
            "id": "investment_loan_term",
            "question": "What is your investment loan term?",
            "subtitle": "Enter the term of your investment loan in years.",
            "type": "number",
            "min": 1,
            "max": 30,
            "category": "financial_info",
            "condition": lambda data: data.get('has_investment_loan') == True
        },
        {
            "id": "has_car_loan",
            "question": "Do you have a car loan?",
            "subtitle": "This helps us understand your current financial obligations.",
            "type": "checkbox",
            "category": "financial_info"
        },
        {
            "id": "car_loan_amount",
            "question": "What is your car loan amount?",
            "subtitle": "Enter the total amount of your car loan.",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "financial_info",
            "condition": lambda data: data.get('has_car_loan') == True
        },
        {
            "id": "has_credit_card_debt",
            "question": "Do you have credit card debt?",
            "subtitle": "This helps us understand your current financial obligations.",
            "type": "checkbox",
            "category": "financial_info"
        },
        {
            "id": "credit_card_debt",
            "question": "What is your credit card debt amount?",
            "subtitle": "Enter the total amount of your credit card debt.",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "financial_info",
            "condition": lambda data: data.get('has_credit_card_debt') == True
        },
        
        # Step 6: Refinance Strategy
        {
            "id": "refinance_count",
            "question": "🔁 How many times would you like to refinance in this plan?",
            "subtitle": "This helps us plan your refinancing strategy.",
            "type": "number",
            "min": 0,
            "max": 10,
            "value": 1,
            "category": "refinance_info"
        },
        {
            "id": "refinance_years",
            "question": "🕓 In which year(s) do you plan to refinance?",
            "subtitle": "Select the years when you plan to refinance.",
            "type": "multiselect",
            "options": list(range(1, 31)),
            "default": [5],
            "category": "refinance_info",
            "condition": lambda data: data.get('refinance_count', 0) > 0
        },
        {
            "id": "other_liabilities",
            "question": "Other Loan Payments ($/month)",
            "subtitle": "",
            "type": "number",
            "min": 0,
            "step": 100,
            "category": "user_info"
        },
        {
            "id": "credit_card_debt",
            "question": "Credit Card Debt ($)",
            "subtitle": "",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "user_info"
        },
        {
            "id": "other_expenses",
            "question": "Other Monthly Expenses ($)",
            "subtitle": "",
            "type": "number",
            "min": 0,
            "step": 100,
            "category": "user_info"
        },
        {
            "id": "emergency_fund",
            "question": "Emergency Fund ($)",
            "subtitle": "",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "user_info"
        },
        {
            "id": "investment_portfolio",
            "question": "Investment Portfolio Value ($)",
            "subtitle": "",
            "type": "number",
            "min": 0,
            "step": 10000,
            "category": "user_info"
        },
        {
            "id": "risk_tolerance",
            "question": "Risk Tolerance",
            "subtitle": "",
            "type": "selectbox",
            "options": ["Conservative", "Moderate", "Aggressive"],
            "category": "user_info"
        },
        {
            "id": "refinance_threshold",
            "question": "Interest Rate Threshold for Refinance (%)",
            "subtitle": "",
            "type": "number",
            "min": 0.0,
            "max": 20.0,
            "step": 0.1,
            "category": "refinance_info"
        },
        {
            "id": "refinance_cost",
            "question": "Expected Refinance Cost ($)",
            "subtitle": "",
            "type": "number",
            "min": 0,
            "step": 1000,
            "category": "refinance_info"
        },
        {
            "id": "target_roi",
            "question": "Target ROI (%)",
            "subtitle": "",
            "type": "number",
            "min": 0.0,
            "max": 100.0,
            "step": 0.5,
            "category": "refinance_info"
        },
        {
            "id": "investment_horizon",
            "question": "Investment Horizon (Years)",
            "subtitle": "",
            "type": "number",
            "min": 1,
            "max": 50,
            "step": 1,
            "category": "refinance_info"
        },
        {
            "id": "exit_strategy",
            "question": "Exit Strategy",
            "subtitle": "",
            "type": "selectbox",
            "options": ["Long-term Hold", "Fix and Flip", "1031 Exchange"],
            "category": "refinance_info"
        }
    ]
    
    # Get current question
    current_step = st.session_state.step - 1
    if current_step < len(questions):
        current_question = questions[current_step]
        
        # 获取 user_info 作为 condition 的上下文
        user_info = st.session_state.current_scenario.get('user_info', {})
        # 检查 condition
        if 'condition' in current_question:
            if not current_question['condition'](user_info):
                st.session_state.step += 1
                st.rerun()
        
        # Display the question
        st.markdown(f'<div class="question">{current_question["question"]}</div>', unsafe_allow_html=True)
        if 'subtitle' in current_question:
            st.markdown(f'<div class="subtitle">{current_question["subtitle"]}</div>', unsafe_allow_html=True)
        
        # Get user input based on question type
        if current_question["type"] == "radio":
            response = st.radio("Select an option", current_question["options"], horizontal=True, label_visibility="collapsed")
        elif current_question["type"] == "checkbox":
            response = st.checkbox("Check this box", label_visibility="collapsed")
        elif current_question["type"] == "number":
            response = st.number_input(
                "Enter a number",
                min_value=current_question.get("min", 0),
                max_value=current_question.get("max", None),
                value=current_question.get("value", 0),
                step=current_question.get("step", 1),
                label_visibility="collapsed"
            )
        elif current_question["type"] == "slider":
            response = st.slider(
                "Select a value",
                min_value=current_question["min"],
                max_value=current_question["max"],
                value=current_question["value"],
                step=current_question["step"],
                label_visibility="collapsed"
            )
        elif current_question["type"] == "selectbox":
            response = st.selectbox("Select an option", current_question["options"], label_visibility="collapsed")
        elif current_question["type"] == "multiselect":
            response = st.multiselect("Select options", current_question["options"], default=current_question["default"], label_visibility="collapsed")
        elif current_question["type"] == "date":
            response = st.date_input("Select a date", label_visibility="collapsed")
        
        # Progress bar
        progress = (current_step + 1) / len(questions)
        st.progress(progress)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous", disabled=current_step == 0):
                st.session_state.step = max(1, st.session_state.step - 1)
                st.rerun()
        
        with col2:
            if st.button("Next"):
                # Save response to session state
                category = current_question["category"]
                if category not in st.session_state.current_scenario:
                    st.session_state.current_scenario[category] = {}
                st.session_state.current_scenario[category][current_question["id"]] = response
                
                # Move to next question
                st.session_state.step += 1
                st.rerun()
    else:
        # All questions completed
        st.success("All information collected!")
        
        # Calculate results
        results = calculator.calculate_all(st.session_state.current_scenario)
        
        # Display results
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">Investment Analysis Results</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Property Value", f"${results.get('property_value', 0):,.2f}")
            st.metric("Total Equity", f"${results.get('total_equity', 0):,.2f}")
        with col2:
            st.metric("Monthly Payment", f"${results.get('monthly_payment', 0):,.2f}")
            st.metric("ROI", f"{results.get('roi', 0):.2%}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Save scenario
        if st.button("Save Scenario"):
            st.session_state.scenarios.append(st.session_state.current_scenario)
            st.session_state.current_scenario = {
                'name': f"Scenario {len(st.session_state.scenarios) + 1}",
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user_info': {},
                'assets': [],
                'refinance_info': {}
            }
            st.session_state.step = 1
            st.rerun()

def show_analysis_page(calculator, visualizer):
    st.header("Investment Analysis")
    
    if not st.session_state.scenarios:
        st.warning("Please complete at least one scenario first.")
        return
    
    # Select scenario to analyze
    scenario_names = [f"{s['name']} ({s['created_at']})" for s in st.session_state.scenarios]
    selected_scenario = st.selectbox("Select Scenario", scenario_names)
    scenario_index = scenario_names.index(selected_scenario)
    
    # Calculate results
    results = calculator.calculate_all(st.session_state.scenarios[scenario_index])
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Metrics")
        st.metric("Total Investment Value", f"${results.get('total_value', 0):,.2f}")
        st.metric("Total Equity", f"${results.get('total_equity', 0):,.2f}")
        st.metric("Monthly Cash Flow", f"${results.get('monthly_cash_flow', 0):,.2f}")
    
    with col2:
        st.subheader("Returns")
        st.metric("ROI", f"{results.get('roi', 0):.2%}")
        st.metric("Cash on Cash Return", f"{results.get('cash_on_cash', 0):.2%}")
        st.metric("Internal Rate of Return", f"{results.get('irr', 0):.2%}")
    
    # Display charts
    st.subheader("Investment Analysis Charts")
    charts = visualizer.create_all_charts(results)
    for chart in charts:
        st.plotly_chart(chart, use_container_width=True)

def show_scenarios_page(calculator, visualizer):
    st.header("Scenario Comparison")
    
    if not st.session_state.scenarios:
        st.warning("Please complete at least one scenario first.")
        return
    
    # Display all scenarios
    for i, scenario in enumerate(st.session_state.scenarios):
        with st.expander(f"{scenario['name']} ({scenario['created_at']})"):
            # Calculate results for this scenario
            results = calculator.calculate_all(scenario)
            
            # Display key metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Property Value", f"${results.get('property_value', 0):,.2f}")
                st.metric("Total Equity", f"${results.get('total_equity', 0):,.2f}")
            with col2:
                st.metric("Monthly Payment", f"${results.get('monthly_payment', 0):,.2f}")
                st.metric("ROI", f"{results.get('roi', 0):.2%}")
            
            # Add delete button
            if st.button(f"Delete Scenario {i+1}"):
                st.session_state.scenarios.pop(i)
                st.rerun()
    
    # Add comparison chart
    if len(st.session_state.scenarios) > 1:
        st.subheader("Scenario Comparison")
        comparison_chart = visualizer.create_comparison_chart(st.session_state.scenarios)
        st.plotly_chart(comparison_chart, use_container_width=True)

def show_assets_page():
    st.header("Asset List")
    assets = st.session_state.current_scenario.get('assets', [])
    if not assets:
        st.info("No assets added yet. Please add property assets in the Input page.")
        return
    for idx, asset in enumerate(assets):
        with st.expander(f"Asset #{idx+1} - {asset.get('property_type', 'Unknown')}"):
            st.write(asset)
            # 未来可扩展：资产修改、删除、退出资产组合、生成报告等
            # if st.button(f"Edit Asset {idx+1}"):
            #     ...
            # if st.button(f"Remove Asset {idx+1}"):
            #     ...

def show_expense_input_page():
    import streamlit as st
    from datetime import date
    st.header("Expense Tracking & Input")
    # 获取资产列表
    assets_list = st.session_state.current_scenario.get('assets', [])
    property_options = [f"Asset #{i+1} - {a.get('property_type', 'Unknown')}" for i, a in enumerate(assets_list)]
    if not property_options:
        st.info("No assets found. Please add property assets first.")
        return
    with st.form("expense_form"):
        description = st.text_input("Expense Description")
        expense_type = st.selectbox("Expense Type", ["One-time", "Property Tax", "Interest", "Home Insurance", "Other", "Depreciable"])
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        date_incurred = st.date_input("Date Incurred", value=date.today())
        property_idx = st.selectbox("Associated Property", property_options)
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            expense = {
                "description": description,
                "expense_type": expense_type,
                "amount": amount,
                "date": str(date_incurred),
                "property_id": property_idx
            }
            if "expenses" not in st.session_state:
                st.session_state.expenses = []
            st.session_state.expenses.append(expense)
            st.success("Expense added!")
    # 展示已录入支出
    if "expenses" in st.session_state and st.session_state.expenses:
        st.subheader("All Expenses")
        st.table(st.session_state.expenses)

def show_data_page():
    st.title("📊 Data Management")
    
    # Property Information
    st.subheader("Property Information")
    properties = get_scenario_properties(1)  # Using scenario_id 1 for now
    if properties:
        for prop in properties:
            with st.expander(f"Property {prop[0]}"):
                st.write(f"Type: {prop[2]}")
                st.write(f"Purchase Price: ${prop[3]:,.2f}")
                st.write(f"Down Payment: ${prop[4]:,.2f}")
                st.write(f"Mortgage Rate: {prop[5]}%")
                st.write(f"Loan Term: {prop[6]} years")
                st.write(f"Rental Income: ${prop[7]:,.2f}")
                st.write(f"Expected Appreciation: {prop[8]}%")
                st.write(f"Vacancy Rate: {prop[9]}%")
    else:
        st.info("No property information available")

    # Income & Expenses
    st.subheader("Income & Expenses")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Expense Records")
        for prop in properties:
            expenses = get_property_expenses(prop[0])
            if expenses:
                for exp in expenses:
                    with st.expander(f"Expense {exp[0]}"):
                        st.write(f"Type: {exp[3]}")
                        st.write(f"Amount: ${exp[4]:,.2f}")
                        st.write(f"Date: {exp[5]}")
            else:
                st.info("No expense records available")
    
    with col2:
        st.write("Income Records")
        for prop in properties:
            incomes = get_property_incomes(prop[0])
            if incomes:
                for inc in incomes:
                    with st.expander(f"Income {inc[0]}"):
                        st.write(f"Type: {inc[3]}")
                        st.write(f"Amount: ${inc[4]:,.2f}")
                        st.write(f"Date: {inc[5]}")
            else:
                st.info("No income records available")

    # Mortgage Information
    st.subheader("Mortgage Information")
    for prop in properties:
        mortgages = get_property_mortgages(prop[0])
        if mortgages:
            for mort in mortgages:
                with st.expander(f"Mortgage {mort[0]}"):
                    st.write(f"Loan Amount: ${mort[2]:,.2f}")
                    st.write(f"Interest Rate: {mort[3]}%")
                    st.write(f"Term: {mort[4]} years")
                    st.write(f"Start Date: {mort[5]}")
                    st.write(f"End Date: {mort[6]}")
        else:
            st.info("No mortgage information available")

def show_household_income_page():
    st.header("Step 1: User Household Information")

    # Check if user info is already saved
    if 'user_info_locked' not in st.session_state:
        st.session_state.user_info_locked = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'scenario_id' not in st.session_state:
        st.session_state.scenario_id = None

    # If locked, show info and allow edit
    if st.session_state.user_info_locked:
        user_data = st.session_state.user_data
        st.success("User information saved!")
        st.write(f"**Household Structure:** {user_data.get('household_type')}")
        st.write(f"**Primary Income:** ${user_data.get('primary_income', 0):,.2f}")
        if user_data.get('household_type') == 'Dual-income':
            st.write(f"**Secondary Income:** ${user_data.get('secondary_income', 0):,.2f}")
        st.write(f"**Retirement Age:** {user_data.get('retirement_age')}")
        st.write(f"**Passive Income Goal:** ${user_data.get('monthly_passive_income', 0):,.2f}/mo")
        if user_data.get('has_net_worth_target') == 'Yes':
            st.write(f"**Net Worth Target:** ${user_data.get('net_worth_target', 0):,.2f}")
        if st.button("Edit"):
            st.session_state.user_info_locked = False
        return

    # Household Structure
    household_type = st.radio(
        "What is your household structure?",
        ["Single-income", "Dual-income"],
        horizontal=True,
        key="household_type"
    )
    # Primary Income
    primary_income = st.number_input(
        "What is your annual income (Person 1)?",
        min_value=0,
        step=10000,
        key="primary_income"
    )
    # Secondary Income (if applicable)
    if household_type == "Dual-income":
        secondary_income = st.number_input(
            "What is your annual income (Person 2)?",
            min_value=0,
            step=10000,
            key="secondary_income"
        )
    else:
        secondary_income = 0
    # Retirement Age
    retirement_age = st.number_input(
        "What age do you plan to retire?",
        min_value=30,
        max_value=80,
        value=65,
        key="retirement_age"
    )
    # Passive Income Goal
    monthly_passive_income = st.number_input(
        "How much monthly passive income do you expect during retirement?",
        min_value=0,
        step=1000,
        key="monthly_passive_income"
    )
    # Net Worth Target
    has_net_worth_target = st.radio(
        "Do you have a net worth target?",
        ["Yes", "No"],
        horizontal=True,
        key="has_net_worth_target"
    )
    if has_net_worth_target == "Yes":
        net_worth_target = st.number_input(
            "What is your net worth target?",
            min_value=0,
            step=100000,
            key="net_worth_target"
        )
    else:
        net_worth_target = 0

    if st.button("Save and Continue"):
        # Save to session state
        st.session_state.user_data.update({
            'household_type': household_type,
            'primary_income': primary_income,
            'secondary_income': secondary_income,
            'retirement_age': retirement_age,
            'monthly_passive_income': monthly_passive_income,
            'has_net_worth_target': has_net_worth_target,
            'net_worth_target': net_worth_target
        })
        # Save to database
        user_id = create_user(email=None, name=None)
        scenario_id = create_scenario(user_id, "Default Scenario", data=None)
        st.session_state.user_id = user_id
        st.session_state.scenario_id = scenario_id
        st.session_state.user_info_locked = True
        st.success("User information saved! You can now proceed to the next step.")
        st.experimental_rerun()

def show_investment_goal_page():
    st.header("Step 2: Investment Goal")
    
    # Retirement Age
    st.subheader("🎯 Retirement Planning")
    retirement_age = st.number_input(
        "What age do you plan to retire?",
        min_value=30,
        max_value=80,
        value=65,
        help="This helps us plan your investment timeline"
    )
    
    # Retirement Income
    monthly_passive_income = st.number_input(
        "How much monthly passive income do you expect during retirement?",
        min_value=0,
        step=1000,
        help="Enter your target monthly passive income"
    )
    
    # Net Worth Target
    st.subheader("💼 Net Worth Target")
    has_net_worth_target = st.radio(
        "Do you have a net worth target?",
        ["Yes", "No"],
        horizontal=True,
        help="For example, $3,000,000 by age 60"
    )
    
    if has_net_worth_target == "Yes":
        net_worth_target = st.number_input(
            "What is your net worth target?",
            min_value=0,
            step=100000,
            help="Enter your target net worth amount"
        )
    else:
        net_worth_target = 0
    
    # Save data to session state
    st.session_state.user_data.update({
        'retirement_age': retirement_age,
        'monthly_passive_income': monthly_passive_income,
        'has_net_worth_target': has_net_worth_target,
        'net_worth_target': net_worth_target
    })

def show_property_planning_page():
    st.header("Step 3: First Property Planning")
    
    # Current Status
    st.subheader("🏡 Property Status")
    property_ownership = st.radio(
        "Do you currently own a home or plan to purchase one?",
        ["Own", "Plan to buy"],
        horizontal=True
    )
    
    # Property Type
    st.subheader("📊 Property Type")
    property_type = st.radio(
        "Is the first property a:",
        ["Principal Residence", "Investment Property"],
        horizontal=True
    )
    
    # Down Payment
    st.subheader("💵 Down Payment")
    has_down_payment = st.radio(
        "Do you already have a down payment saved?",
        ["Yes", "No"],
        horizontal=True
    )
    
    if has_down_payment == "Yes":
        down_payment = st.number_input(
            "How much is your down payment?",
            min_value=0,
            step=10000
        )
    else:
        yearly_savings = st.number_input(
            "How much can you save yearly for the down payment?",
            min_value=0,
            step=1000
        )
        savings_years = st.number_input(
            "For how many years will you save?",
            min_value=1,
            max_value=30
        )
        down_payment = yearly_savings * savings_years
    
    # Property Details
    st.subheader("🏠 Property Details")
    purchase_price = st.number_input(
        "What is your budget or target price for the first property?",
        min_value=0,
        step=10000
    )
    
    closing_date = st.date_input(
        "What is the expected closing date?",
        min_value=datetime.now()
    )
    
    same_mortgage_date = st.checkbox(
        "Is the mortgage start date the same as the closing date?"
    )
    
    if not same_mortgage_date:
        mortgage_start_date = st.date_input(
            "When will your mortgage start?",
            min_value=datetime.now()
        )
    else:
        mortgage_start_date = closing_date
    
    # Mortgage Details
    st.subheader("🏦 Mortgage Details")
    mortgage_rate = st.number_input(
        "What is the expected mortgage interest rate? (%)",
        min_value=0.0,
        max_value=20.0,
        value=5.0,
        step=0.1
    )
    
    amortization = st.selectbox(
        "What is the amortization period?",
        [20, 25, 30]
    )
    
    loan_term = st.selectbox(
        "What is the loan term (fixed rate period)?",
        [1, 2, 3, 4, 5]
    )
    
    # Save data to session state
    st.session_state.user_data.update({
        'property_ownership': property_ownership,
        'property_type': property_type,
        'has_down_payment': has_down_payment,
        'down_payment': down_payment,
        'purchase_price': purchase_price,
        'closing_date': closing_date,
        'mortgage_start_date': mortgage_start_date,
        'mortgage_rate': mortgage_rate,
        'amortization': amortization,
        'loan_term': loan_term
    })

def show_rent_growth_page():
    st.header("Step 4: Rent & Property Growth Assumptions")
    
    if st.session_state.user_data.get('property_type') == "Investment Property":
        # Rental Input Type
        st.subheader("💼 Rental Information")
        rent_input_type = st.radio(
            "Will you input actual rent or use estimated rental yield?",
            ["Input actual rent", "Use rental yield"],
            horizontal=True
        )
        
        if rent_input_type == "Input actual rent":
            monthly_rent = st.number_input(
                "What monthly rent do you expect?",
                min_value=0,
                step=100
            )
        else:
            rental_yield = st.number_input(
                "What rental yield do you expect? (%)",
                min_value=0.0,
                max_value=20.0,
                step=0.1
            )
            monthly_rent = (st.session_state.user_data['purchase_price'] * rental_yield / 100) / 12
    
    # Property Growth
    st.subheader("📈 Property Growth")
    appreciation_rate = st.slider(
        "Expected annual property appreciation rate?",
        min_value=0.0,
        max_value=20.0,
        value=3.0,
        step=0.1
    )
    
    if st.session_state.user_data.get('property_type') == "Investment Property":
        vacancy_rate = st.slider(
            "Expected vacancy rate?",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.1
        )
    
    # Expenses
    st.subheader("🧾 Property Expenses")
    expense_type = st.radio(
        "How would you like to input property expenses?",
        ["Percentage of property value", "Actual amount"],
        horizontal=True
    )
    
    if expense_type == "Percentage of property value":
        expense_rate = st.number_input(
            "What annual expense rate do you expect? (%)",
            min_value=0.0,
            max_value=10.0,
            value=1.0,
            step=0.1
        )
        annual_expenses = st.session_state.user_data['purchase_price'] * expense_rate / 100
    else:
        annual_expenses = st.number_input(
            "What annual expenses do you expect?",
            min_value=0,
            step=1000
        )
    
    # Save data to session state
    st.session_state.user_data.update({
        'rent_input_type': rent_input_type if st.session_state.user_data.get('property_type') == "Investment Property" else None,
        'monthly_rent': monthly_rent if st.session_state.user_data.get('property_type') == "Investment Property" else 0,
        'appreciation_rate': appreciation_rate,
        'vacancy_rate': vacancy_rate if st.session_state.user_data.get('property_type') == "Investment Property" else 0,
        'expense_type': expense_type,
        'annual_expenses': annual_expenses
    })

def show_financial_info_page():
    st.header("Step 5: Other Financial Information")
    
    # Investment Loan
    st.subheader("💸 Investment Loan")
    has_investment_loan = st.checkbox("Do you have an investment loan?")
    
    if has_investment_loan:
        investment_loan_amount = st.number_input(
            "What is your investment loan amount?",
            min_value=0,
            step=10000
        )
        investment_loan_start_date = st.date_input(
            "When did your investment loan start?",
            min_value=datetime.now() - timedelta(days=365*30)
        )
        investment_loan_rate = st.number_input(
            "What is your investment loan interest rate? (%)",
            min_value=0.0,
            max_value=20.0,
            step=0.1
        )
        investment_loan_payment = st.number_input(
            "What is your monthly investment loan payment?",
            min_value=0,
            step=100
        )
        investment_loan_term = st.number_input(
            "What is your investment loan term? (years)",
            min_value=1,
            max_value=30
        )
    
    # Car Loan
    st.subheader("🚗 Car Loan")
    has_car_loan = st.checkbox("Do you have a car loan?")
    
    if has_car_loan:
        car_loan_amount = st.number_input(
            "What is your car loan amount?",
            min_value=0,
            step=1000
        )
    
    # Credit Card Debt
    st.subheader("💳 Credit Card Debt")
    has_credit_card_debt = st.checkbox("Do you have credit card debt?")
    
    if has_credit_card_debt:
        credit_card_debt = st.number_input(
            "What is your credit card debt amount?",
            min_value=0,
            step=1000
        )
    
    # Save data to session state
    st.session_state.user_data.update({
        'has_investment_loan': has_investment_loan,
        'investment_loan_amount': investment_loan_amount if has_investment_loan else 0,
        'investment_loan_start_date': investment_loan_start_date if has_investment_loan else None,
        'investment_loan_rate': investment_loan_rate if has_investment_loan else 0,
        'investment_loan_payment': investment_loan_payment if has_investment_loan else 0,
        'investment_loan_term': investment_loan_term if has_investment_loan else 0,
        'has_car_loan': has_car_loan,
        'car_loan_amount': car_loan_amount if has_car_loan else 0,
        'has_credit_card_debt': has_credit_card_debt,
        'credit_card_debt': credit_card_debt if has_credit_card_debt else 0
    })

def show_refinance_strategy_page():
    st.header("Step 6: Refinance Strategy")
    
    # Refinance Count
    st.subheader("🔁 Refinance Plan")
    refinance_count = st.number_input(
        "How many times would you like to refinance in this plan?",
        min_value=0,
        max_value=10,
        value=1
    )
    
    if refinance_count > 0:
        refinance_years = st.multiselect(
            "In which year(s) do you plan to refinance?",
            options=list(range(1, 31)),
            default=[5]
        )
    
    # Save data to session state
    st.session_state.user_data.update({
        'refinance_count': refinance_count,
        'refinance_years': refinance_years if refinance_count > 0 else []
    })

if __name__ == "__main__":
    main() 