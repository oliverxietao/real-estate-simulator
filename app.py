import streamlit as st
from src.input_handler import InputHandler
from src.calculator import InvestmentCalculator
from src.visualizer import DataVisualizer
from src.report_generator import ReportGenerator
import json
from datetime import datetime, timedelta
from src.db import init_db

def main():
    st.set_page_config(
        page_title="Real Estate Investment Return Simulator",
        page_icon="🏠",
        layout="centered"
    )
    
    # Custom CSS for Apple-style design with dark mode support
    st.markdown("""
        <style>
        /* Base styles */
        .stApp {
            max-width: 800px;
            margin: 0 auto;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
            }
            .question {
                color: #fff !important;
                font-weight: 700 !important;
                text-shadow: 0 1px 4px #0008;
            }
            .subtitle {
                color: #e0e0e0 !important;
                font-weight: 400;
            }
            .stRadio > div {
                background-color: #23232b !important;
                color: #fff !important;
                border: 1px solid #444 !important;
                box-shadow: 0 2px 8px #0002;
            }
            .stRadio > div:hover {
                background-color: #33334a !important;
            }
            .stNumberInput > div > div > input {
                background-color: #23232b !important;
                color: #fff !important;
                border-color: #4d4d4d !important;
            }
            .stNumberInput > div > div > input:focus {
                border-color: #0071e3 !important;
                box-shadow: 0 0 0 4px rgba(0,113,227,0.2) !important;
            }
            .stSlider > div > div > div {
                background-color: #0071e3 !important;
            }
            .stSlider > div > div > div > div {
                background-color: #0071e3 !important;
            }
            .stProgress > div > div > div {
                background-color: #0071e3 !important;
            }
            .phase-title {
                color: #fff !important;
                border-bottom-color: #4d4d4d !important;
            }
            .result-box {
                background-color: #23232b !important;
                border: 1px solid #4d4d4d !important;
            }
            .result-title {
                color: #fff !important;
            }
            .result-value {
                color: #4da3ff !important;
            }
            .scenario-box {
                background-color: #23232b !important;
                border: 1px solid #4d4d4d !important;
            }
            .scenario-box:hover {
                border-color: #0071e3 !important;
                box-shadow: 0 0 0 4px rgba(0,113,227,0.2) !important;
            }
            /* Metric cards */
            .stMetric {
                background-color: #23232b !important;
                border: 1px solid #4d4d4d !important;
                border-radius: 12px;
                padding: 15px;
            }
            .stMetric:hover {
                border-color: #0071e3 !important;
                box-shadow: 0 0 0 4px rgba(0,113,227,0.2) !important;
            }
            /* Form elements */
            .stSelectbox > div > div {
                background-color: #23232b !important;
                color: #fff !important;
            }
            .stDateInput > div > div > input {
                background-color: #23232b !important;
                color: #fff !important;
                border-color: #4d4d4d !important;
            }
            /* Buttons */
            .stButton > button {
                background-color: #0071e3 !important;
                color: #fff !important;
            }
            .stButton > button:hover {
                background-color: #0077ed !important;
            }
            /* Success message */
            .stSuccess {
                background-color: #1a472a !important;
                color: #fff !important;
            }
            /* Warning message */
            .stWarning {
                background-color: #472a1a !important;
                color: #fff !important;
            }
        }
        
        /* Light mode styles */
        .question {
            font-size: 28px;
            font-weight: 500;
            margin-bottom: 30px;
            color: #1d1d1f;
            line-height: 1.3;
        }
        
        .subtitle {
            font-size: 17px;
            color: #86868b;
            margin-bottom: 30px;
            line-height: 1.4;
        }
        
        .stButton>button {
            background-color: #0071e3;
            color: white;
            border-radius: 20px;
            padding: 12px 24px;
            font-size: 17px;
            border: none;
            width: 100%;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #0077ed;
            transform: scale(1.02);
        }
        
        .stRadio > div {
            padding: 20px;
            border-radius: 12px;
            background-color: #f5f5f7;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }
        
        .stRadio > div:hover {
            background-color: #e8e8ed;
            transform: scale(1.01);
        }
        
        .stNumberInput > div > div > input {
            border-radius: 12px;
            padding: 12px;
            font-size: 17px;
            border: 1px solid #d2d2d7;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: #0071e3;
            box-shadow: 0 0 0 4px rgba(0,113,227,0.1);
        }
        
        .stSlider > div > div > div {
            background-color: #0071e3;
        }
        
        .stSlider > div > div > div > div {
            background-color: #0071e3;
        }
        
        .stProgress > div > div > div {
            background-color: #0071e3;
        }
        
        .phase-title {
            font-size: 24px;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #d2d2d7;
        }
        
        .result-box {
            background-color: #f5f5f7;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .result-title {
            font-size: 20px;
            font-weight: 500;
            color: #1d1d1f;
            margin-bottom: 10px;
        }
        
        .result-value {
            font-size: 24px;
            font-weight: 600;
            color: #0071e3;
        }
        
        .scenario-box {
            background-color: #f5f5f7;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid #d2d2d7;
        }
        
        .scenario-box:hover {
            border-color: #0071e3;
            box-shadow: 0 0 0 4px rgba(0,113,227,0.1);
        }
        
        /* Metric cards */
        .stMetric {
            background-color: #f5f5f7;
            border: 1px solid #d2d2d7;
            border-radius: 12px;
            padding: 15px;
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            border-color: #0071e3;
            box-shadow: 0 0 0 4px rgba(0,113,227,0.1);
        }
        
        /* Form elements */
        .stSelectbox > div > div {
            background-color: #ffffff;
            border: 1px solid #d2d2d7;
            border-radius: 12px;
        }
        
        .stDateInput > div > div > input {
            background-color: #ffffff;
            border: 1px solid #d2d2d7;
            border-radius: 12px;
        }
        
        /* Success message */
        .stSuccess {
            background-color: #e6f3e6;
            color: #1a472a;
        }
        
        /* Warning message */
        .stWarning {
            background-color: #f3e6e6;
            color: #472a1a;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = {
            'name': f"Scenario {len(st.session_state.scenarios) + 1}",
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_info': {},
            'assets': []
        }
    if 'current_asset' not in st.session_state:
        st.session_state.current_asset = {}
    if 'asset_step' not in st.session_state:
        st.session_state.asset_step = 1
    
    # Initialize components
    input_handler = InputHandler()
    calculator = InvestmentCalculator()
    visualizer = DataVisualizer()
    report_generator = ReportGenerator()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Input", "Assets", "Analysis", "Scenarios", "Expenses"])
    
    if page == "Input":
        show_input_page(input_handler, calculator)
    elif page == "Assets":
        show_assets_page()
    elif page == "Analysis":
        show_analysis_page(calculator, visualizer)
    elif page == "Scenarios":
        show_scenarios_page(calculator, visualizer)
    elif page == "Expenses":
        show_expense_input_page()

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

if __name__ == "__main__":
    init_db()
    main() 