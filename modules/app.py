import streamlit as st
import pydeck as pdk
import requests
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import sqlite3
import hashlib
import time
import io

# Gemini API Setup
GOOGLE_API_KEY = "AIzaSyCL80IskILPHHLm93Npr-6w9TFMw8YIdWQ"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
version = 'models/gemini-1.5-flash'
system_prompt = '''
Тебя зовут Амина, ты эксперт в сфере финансов и помогаешь школьникам и студентам по развитию навыков финансовой грамотности!
Если тебе будут задавать вопросы не по финансом, отвечай, что не знаешь.
Будь вежливым и очень любезным!
Отвечай кратко и четко!
'''

model = genai.GenerativeModel(model_name=version, system_instruction=system_prompt)

# Payment Modal Function
def show_payment_modal(plan_type):
    st.markdown("""
        <style>
        .payment-modal {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .payment-field {
            margin: 10px 0;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='payment-modal'>", unsafe_allow_html=True)
        st.subheader("Payment Details")
        
        # Plan details
        amount = "50.00" if plan_type == "yearly" else "5.00"
        st.write(f"Selected Plan: {plan_type.capitalize()}")
        st.write(f"Amount: ${amount}")
        
        # Card details
        col1, col2 = st.columns(2)
        with col1:
            card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            expiry = st.text_input("Expiry Date", placeholder="MM/YY")
        with col2:
            card_holder = st.text_input("Card Holder Name", placeholder="John Doe")
            cvv = st.text_input("CVV", placeholder="123", type="password")
            
        # Billing address
        st.subheader("Billing Address")
        address = st.text_area("Address")
        col3, col4 = st.columns(2)
        with col3:
            city = st.text_input("City")
            country = st.selectbox("Country", ["Kazakhstan", "Russia", "Other"])
        with col4:
            postal_code = st.text_input("Postal Code")
            
        if st.button("Process Payment"):
            # Simulate payment processing
            with st.spinner("Processing payment..."):
                import time
                time.sleep(2)
                st.success("Payment processed successfully!")
                st.balloons()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Education Hub Function
def education_hub():
    st.title("Education Hub")
    
    # Course structure
    lessons = {
        "Introduction to Money": {
            "video_url": "https://youtu.be/btZ43QLlj40?si=-ycmNygL3TalCx0Q",
            "content": """
            ### Learning Objectives
            - Understanding the concept of money
            - History of money in Kazakhstan
            - Modern banking system
            
            ### Key Points
            1. Definition of money and its functions
            2. Evolution from barter to digital currencies
            3. Role of the National Bank of Kazakhstan
            """,
            "quiz": [
        {
            "question": "What are the three main functions of money?",
            "options": [
                "Medium of exchange, store of value, unit of account",
                "Spending, saving, investing",
                "Gold, silver, paper"
            ],
            "correct": 0
        },
        {
            "question": "Which function of money allows it to be used to purchase goods and services?",
            "options": [
                "Store of value",
                "Medium of exchange",
                "Unit of account"
            ],
            "correct": 1
        },
        {
            "question": "What function of money ensures that it retains its value over time?",
            "options": [
                "Medium of exchange",
                "Store of value",
                "Unit of account"
            ],
            "correct": 1
        },
        {
            "question": "How does money serve as a unit of account?",
            "options": [
                "By providing a standard measure for pricing goods and services.",
                "By allowing people to save for future purchases.",
                "By facilitating trade between different currencies."
            ],
            "correct": 0
        },
        {
            "question": "What is an example of money functioning as a store of value?",
            "options": [
                "Using cash to buy groceries.",
                "Saving money in a bank account.",
                "Exchanging money for stocks."
            ],
            "correct": 1
        },
        {
            "question": "Why is it important for money to act as a medium of exchange?",
            "options": [
                "It helps in measuring economic growth.",
                "It simplifies transactions by eliminating bartering.",
                "It ensures that prices remain stable."
            ],
            "correct": 1
        },
        {
            "question": "In what way does money function as a unit of account?",
            "options": [
                "It allows people to compare the value of different goods.",
                "It helps in saving for future expenses.",
                "It provides a means to invest in assets."
            ],
            "correct": 0
        },
        {
            "question": "What happens if money loses its ability to be a store of value?",
            "options": [
                "People will stop using it as a medium of exchange.",
                "It will still function as a unit of account.",
                "Its purchasing power will increase."
            ],
            "correct": 0
        },
        {
            "question": "'Gold, silver, and paper' are examples of what aspect related to money?",
            "options": [
                "Types of currency",
                "Functions of money",
                "Forms of investment"
            ],
            "correct": 0
        },
        {
            "question": "'Spending, saving, and investing' are activities related to which concept?",
            "options": [
                "'Functions' of money",
                "'Uses' of money",
                "'Forms' of currency"
            ],
            "correct": 1
        }
    ]
        },
        "Budgeting Basics": {
            "video_url": "https://youtu.be/sVKQn2I4HDM?si=0jHQ7Zk2pWs0-CuH",
            "content": """
            ### Learning Objectives
            - Creating a personal budget
            - Understanding income and expenses
            - Saving strategies
            
            ### Key Points
            1. 50/30/20 budgeting rule
            2. Fixed vs. variable expenses
            3. Emergency fund importance
            """,
            "quiz": [
        {
            "question": "What percentage should go to needs in the 50/30/20 rule?",
            "options": ["50%", "30%", "20%"],
            "correct": 0
        },
        {
            "question": "In the 50/30/20 rule, what percentage is allocated for wants?",
            "options": ["50%", "30%", "20%"],
            "correct": 1
        },
        {
            "question": "According to the 50/30/20 rule, what percentage should be saved or invested?",
            "options": ["50%", "30%", "20%"],
            "correct": 2
        },
        {
            "question": "Which of the following expenses would typically fall under 'needs' in the 50/30/20 rule?",
            "options": ["Luxury vacations", "Rent or mortgage payments", "Dining out"],
            "correct": 1
        },
        {
            "question": "What is the primary purpose of the 50/30/20 budgeting rule?",
            "options": [
                "To eliminate all debt immediately.",
                "To create a balanced approach to spending and saving.",
                "To maximize investment returns."
            ],
            "correct": 1
        },
        {
            "question": "If someone spends 40% on needs, what percentage should they ideally adjust in wants and savings according to the 50/30/20 rule?",
            "options": [
                "Increase savings to 30%, reduce wants to 20%.",
                "Reduce needs to 30%, keep wants at 20%.",
                "Keep needs at 40%, reduce wants to 10%, increase savings to 30%."
            ],
            "correct": 2
        },
        {
            "question": "What type of expenses are categorized as 'wants' in the 50/30/20 rule?",
            "options": [
                "Utilities and groceries.",
                "Gym memberships and entertainment.",
                "Insurance and taxes."
            ],
            "correct": 1
        },
        {
            "question": "How can someone effectively implement the 50/30/20 rule?",
            "options": [
                "By tracking all expenses and categorizing them accordingly.",
                "By ignoring small purchases.",
                "By only focusing on monthly income."
            ],
            "correct": 0
        },
        {
            "question": "What is a common mistake people make when following the 50/30/20 rule?",
            "options": [
                "Not adjusting their budget based on changing income.",
                "Saving too much money.",
                "Spending too little on needs."
            ],
            "correct": 0
        },
        {
            "question": "'Savings' in the context of the 50/30/20 rule can include which of the following?",
            "options": [
                "Emergency fund contributions and retirement savings.",
                "All discretionary spending.",
                "Only cash savings."
            ],
            "correct": 0
        }
    ]
        },
        "Saving and investing": {
            "video_url": "https://youtu.be/Gu8NlynXRc0?si=1ATtfzgwmtpcnlhH",
            "content": """
            ### Learning Objectives
            - The basics of saving
            - Investment vehicles
            - Long-Term Investment Strategies


            ### Key Points 
            - Building an Emergency Fund
            - The Power of Compounding
            - Diversification and Risk Management
            """,
        "quiz": [
        {
            "question": "What is the most effective way to balance saving money and investing for long-term growth?",
            "options": [
                "Save all your money in a savings account and avoid investing.",
                "Invest in high-risk stocks for maximum returns while saving very little.",
                "Create a balanced strategy by saving for emergencies and investing in diversified assets for long-term growth."
            ],
            "correct": 2
        },
        {
            "question": "How can you ensure that your savings are protected while still growing?",
            "options": [
                "Keep all your savings in cash under your mattress.",
                "Invest only in volatile assets without any savings.",
                "Use a high-yield savings account or a mix of savings and conservative investments."
            ],
            "correct": 2
        },
        {
            "question": "What is a good rule of thumb for how much to save before you start investing?",
            "options": [
                "Save at least 3-6 months' worth of living expenses.",
                "Save as much as possible without any specific target.",
                "There is no need to save before investing."
            ],
            "correct": 0
        },
        {
            "question": "What should be prioritized when creating a financial plan?",
            "options": [
                "Maximizing returns on investments without considering risks.",
                "Building an emergency fund before making any investments.",
                "Investing in the latest trends without a solid plan."
            ],
            "correct": 1
        },
        {
            "question": "Which investment strategy is generally considered the safest?",
            "options": [
                "Investing solely in cryptocurrency.",
                "Diversifying your portfolio across various asset classes.",
                "Putting all your money into one high-risk stock."
            ],
            "correct": 1
        },
        {
            "question": "How often should you review your financial goals and investment strategy?",
            "options": [
                "Only once a year.",
                "Whenever you feel like it.",
                "At least once every six months or after major life changes."
            ],
            "correct": 2
        },
        {
            "question": "What is one benefit of having a diversified investment portfolio?",
            "options": [
                "It guarantees high returns.",
                "It reduces risk by spreading investments across different assets.",
                "It eliminates the need for saving."
            ],
            "correct": 1
        },
        {
            "question": "Why is it important to have an emergency fund?",
            "options": [
                "To take advantage of investment opportunities immediately.",
                "To cover unexpected expenses without going into debt.",
                "To avoid paying taxes on your savings."
            ],
            "correct": 1
        },
        {
            "question": "What is the impact of inflation on savings?",
            "options": [
                "Inflation has no effect on savings.",
                "Inflation decreases the purchasing power of saved money over time.",
                "Inflation increases the value of cash savings."
            ],
            "correct": 1
        },
        {
            "question": "What is an ideal percentage of income to save for retirement?",
            "options": [
                "At least 15% of your income.",
                "Only what is left after spending.",
                "No need to save for retirement if you have other investments."
            ],
            "correct": 0
        }
    ]
        },
        "Debt Management": {
            "video_url":"https://youtu.be/CHiOBzqcMV8?si=hbeUMbrezYROXxfI",
            "content": """
            ### Learning Objectives
            - Understanding Debt Types
            - Debt Repayment Strategies
            - Negotiating with Creditors
            

            ### Key Points 
            - Understanding Debt Types
            - Creating a Debt Repayment Plan
            - Avoiding New Debt
            """,
            "quiz": [
                {"question": "What is the most important step to take when managing personal debt?",
                    "options": ["Ignore the debt and hope it will go away over time.", "Focus on paying off high-interest debt first while making minimum payments on other debts.", "Take out more loans to cover existing debts."],
                    "correct": 1},
                {"question": "What is the primary goal of debt management?",
                    "options": ["To accumulate more debt", "To reduce or eliminate debt efficiently and responsibly", "To avoid paying any interest on loans"],
                    "correct": 1},
                {"question": "Which of the following strategies is recommended for paying off high-interest debt first?",
                    "options": ["Debt snowball method", "Debt avalanche method", "Paying only the minimum balance"],
                    "correct": 1},
                {"question": "What is a key advantage of consolidating multiple debts into a single loan?",
                    "options": ["Ignore the debt and hope it will go away over time.", "Focus on paying off high-interest debt first while making minimum payments on other debts.", "Take out more loans to cover existing debts."],
                    "correct": 1},
                {"question": "What is the most important step to take when managing personal debt?",
                    "options": [
                    "Ignore the debt and hope it will go away over time.",
                    "Focus on paying off high-interest debt first while making minimum payments on other debts.",
                    "Take out more loans to cover existing debts."],
                    "correct": 1},
                {"question": "What method is most effective for reducing debt burden?",
                    "options": [
                    "Only pay the minimum amounts on all debts.",
                    "Create a budget and allocate funds for debt repayment.",
                    "Postpone payments until next month."],
                    "correct": 1},
                {"question": "What should you do first if you have multiple debts?",
                    "options": [
                    "Focus on paying off the smallest debt to eliminate it quickly.",
                    "Pay off the debt with the highest interest rate.",
                    "Ignore all debts and wait for them to disappear."],
                    "correct": 1},
                {"question": "What approach can help avoid accumulating new debts?",
                    "options": [
                    "Use credit cards for all purchases.",
                    "Create an emergency fund for unexpected expenses.",
                    "Ignore financial planning."],
                    "correct": 1},
                {"question": "Which of the following steps can help improve your credit score?",
                    "options": [
                    "Regularly check your credit report and correct any errors.",
                    "Stop paying your debts for several months.",
                    "Close all old credit cards."],
                    "correct": 0},
                {"question": "What should you do if you can't manage your debts on your own?",
                    "options": [
                    "Seek help from a financial advisor or a consumer protection agency.",
                    "Continue to ignore the problem and hope it resolves itself.",
                    "Take out a new loan to pay off old ones."],
                    "correct": 0}
                ]
        },
        "Tax Planning": {
            "video_url":"https://youtu.be/6pEkMBQJc6A?si=kBz6Em5-kjkctsUZ",
            "content": """
            ### Learning Objectives
            - Understand the basics of tax obligations and types of taxes.
            - Learn strategies for legally reducing tax liabilities.
            - Identify tax deductions, credits, and benefits available to individuals and businesses.
            - Develop skills for effective tax planning to maximize after-tax income.
            - Recognize the importance of tax planning in achieving financial goals.

            ### Key Points 
            - Types of Taxes
            - Tax Reduction Strategies
            - Timing of Income and Expenses
            - Retirement and Investment Accounts
            - Record-Keeping
            - Legal Compliance
            """,
            "quiz": [
                {"question": "Anna earns $60,000 per year. She qualifies for a $4,000 tax deduction for charitable donations. If she is in the 25% tax bracket, how much will she save on her taxes with this deduction?",
                    "options": ["$500", "$1000", "$1500"],
                    "correct": 2},
                {"question": "What is the primary goal of tax planning?",
                    "options": ["To minimize tax liability and maximize tax benefits", "To delay paying taxes indefinitely", "To avoid taxes entirely"],
                    "correct": 0},
                {"question": "Which of the following is an example of a tax-deductible expense?",
                    "options": ["Daily coffee purchases", "Mortgage interest payments", "Luxury vacation expenses"],
                    "correct": 1},
                {"question": "What is a tax credit?",
                    "options": ["A reduction in the total amount of tax owed", "A tax deduction that reduces taxable income", "An amount paid to the government to reduce tax rates"],
                    "correct": 0},
                {"question": "Which of the following is an example of tax avoidance?",
                    "options": ["Using offshore tax shelters to evade paying taxes", "Claiming legitimate tax deductions and credits", "Failing to file a tax return"],
                    "correct": 1},
                {"question": "What is the purpose of a tax deferral strategy?",
                    "options": ["To avoid paying taxes at all", "To delay paying taxes to a future date, often when your tax rate may be lower", "To pay more taxes upfront"],
                    "correct": 1},
                {"question": "What type of income is typically taxed at a lower rate?",
                    "options": ["Ordinary income (such as wages and salary)", "Capital gains (profits from the sale of investments held longer than a year)", "Unreported income"],
                    "correct": 1},
                {"question": "Which of the following is a benefit of contributing to a retirement account in tax planning?",
                    "options": ["Contributions are tax-deductible, reducing taxable income in the current year", "Contributions are not taxed, even when withdrawn", "Contributions increase the tax rate you pay in retirement"],
                    "correct": 0},
                {"question": "What is tax evasion?",
                    "options": ["Using legal strategies to minimize tax liability", "Illegally avoiding paying taxes by underreporting income or inflating deductions", "Filing tax returns late without penalties"],
                    "correct": 1},
                {"question": "Which of the following can help reduce taxable income?",
                    "options": ["Increasing income without any deductions", "Contributing to a tax-deferred retirement account", "Ignoring tax laws"],
                    "correct": 1},
            ]
        },
        "Financial Planning": {
            "video_url":"https://youtu.be/AobL1x2N0FI?si=_ml142qaAmw6QqFD",
            "content": """
            ### Learning Objectives
            - Understand the purpose and benefits of financial planning for achieving long-term goals.
            - Identify and set realistic short-term, medium-term, and long-term financial goals.
            - Learn how to create a personal budget to track income, expenses, and savings.
            - Understand the role of emergency funds and how to build them.
            - Develop skills for managing investments, debt, and savings effectively.
            - Recognize the importance of retirement planning and explore different retirement savings options.
            - Learn how to adjust financial plans based on changing life circumstances and goals.

            ### Key Points 
            - Goal Setting
            - Budgeting 
            - Emergency Fund 
            - Investment
            - Retirement Planning
            - Regular Review
            """,
            "quiz": [
    {"question": "What part of a financial plan is essential for covering unexpected expenses?",
        "options": ["Investment portfolio", "Travel budget", "Emergency fund"],
        "correct": 2 },
    {"question": "What is the primary purpose of creating a financial plan?",
        "options": ["To track monthly expenses", "To avoid paying taxes", "To set and achieve long-term financial goals"],
        "correct": 2 },
    {"question": "What is the first step in creating a financial plan?",
        "options": ["Set up an investment account", "Identify your financial goals", "Pay off existing debts"],
        "correct": 1 },
    {"question": "Which of the following is a key component of an emergency fund?",
        "options": ["It should be invested in stocks for high returns", "It should cover at least 3-6 months of living expenses", " It should be used for luxury purchases"],
        "correct": 1 },
    {"question": "What percentage of your income should ideally go toward savings and investments?",
        "options": ["10-15%", "50-60%", "20-30%"],
        "correct": 2 },
    {"question": "What is a major benefit of diversifying your investment portfolio?",
        "options": ["It guarantees no financial risk", "It helps protect against potential market fluctuations", "It allows you to focus on one type of investment"],
        "correct": 1 },
    {"question": "Why is it important to review your financial plan periodically?",
        "options": ["To ensure it is still aligned with your financial goals", "To check if you need to increase your monthly spending", "To calculate how much interest you owe on loans"],
        "correct": 0 },
    {"question": "What is the role of insurance in financial planning?",
        "options": ["It ensures you pay fewer taxes", "It helps protect against unexpected financial losses", "It guarantees a high return on investment"],
        "correct": 1 },
    {"question": "Which of the following is the most effective strategy for managing debt?",
        "options": ["Pay off the smallest debts first", "Ignore high-interest debts and focus on the low-interest ones", "Use a balance transfer credit card for all debts"],
        "correct": 0 },
    {"question": "What is the purpose of setting a budget in financial planning?",
        "options": ["To track your expenses and avoid overspending", "To calculate your net worth", "To increase your investment returns"],
        "correct": 0 },
            ]
        },
    }
    
    # Lesson selection
    selected_lesson = st.selectbox("Select Lesson", list(lessons.keys()))
    
    # Display lesson content
    lesson = lessons[selected_lesson]
    
    # Video section
    st.video(lesson["video_url"])
    
    # Content section
    st.markdown(lesson["content"])
    
    # Interactive elements
    with st.expander("Take Quiz"):
        for i, quiz in enumerate(lesson["quiz"]):
            st.write(f"Question {i+1}: {quiz['question']}")
            answer = st.radio(f"Select answer for question {i+1}:", 
                            quiz["options"],
                            key=f"quiz_{selected_lesson}_{i}")
            
            if st.button(f"Check Answer {i+1}", key=f"check_{i}"):
                if quiz["options"].index(answer) == quiz["correct"]:
                    st.success("Correct!")
                else:
                    st.error("Try again!")
    
    # Progress tracking
    if st.button("Mark as Complete"):
        st.success(f"Lesson '{selected_lesson}' marked as complete!")

# Interactive Maps Function
def interactive_maps():
    st.title("Financial Statistics in Kazakhstan")
    
    # Данные
    regions_data = pd.DataFrame({
        'Region': ['Атырауская область', 'Мангистаунская область', 'Улытау', 'Астана', 'Алматы', 'Актюбинская область', 'Западно-Казахстанская область', 'Атырау', 'Шымкент'],
        'Average_Income': [594296, 579838, 529880, 518495, 480431, 455000, 435000, 400000, 394000],
        'Financial_Literacy_Score': [70, 60, 50, 70, 80, 55, 65, 60, 65],
        'Bank_Branches': [120, 100, 80, 60, 70, 50, 40, 30, 20],
        'ATM_Count': [500, 450, 300, 250, 280, 200, 150, 120, 100]
    })

    cities_data = [
        {"name": "Атырауская область", "latitude": 42.1759, "longitude": 69.3559, "link": "https://ru.wikipedia.org/wiki/Атырауская_область"},
        {"name": "Мангистауская область", "latitude": 43.52, "longitude": 52.00, "link": "https://ru.wikipedia.org/wiki/Мангистауская_область"},
        {"name": "Улытау", "latitude": 48.3652, "longitude": 67.0010, "link": "https://ru.wikipedia.org/wiki/Улытау"},
        {"name": "Астана", "latitude": 51.08, "longitude": 71.26, "link": "https://ru.wikipedia.org/wiki/Астана"},
        {"name": "Алматы", "latitude": 43.15, "longitude": 76.54, "link": "https://ru.wikipedia.org/wiki/Алматы"},
        {"name": "Актюбинская область", "latitude": 50.17, "longitude": 57.10, "link": "https://ru.wikipedia.org/wiki/Актюбинская_область"},
        {"name": "Западно-Казахстанская область", "latitude": 51.14, "longitude": 51.22, "link": "https://ru.wikipedia.org/wiki/Западно-Казахстанская_область"},
        {"name": "Атырау", "latitude": 47.1167, "longitude": 51.8833, "link": "https://ru.wikipedia.org/wiki/Атырау"},
        {"name": "Шымкент", "latitude": 42.18, "longitude": 69.36, "link": "https://ru.wikipedia.org/wiki/Шымкент"}
    ]
    df = pd.DataFrame(cities_data)

    # Выбор типа визуализации
    viz_type = st.selectbox(
        "Select Visualization",
        ["Financial Literacy Score", "Average Income", "Banking Infrastructure"]
    )

    if viz_type == "Financial Literacy Score":
        # Карта
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position="[longitude, latitude]",
            get_radius=50000,
            get_fill_color=[0, 255, 0],
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=48.0,
            longitude=66.0,
            zoom=3
        )

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v10",
                initial_view_state=view_state,
                layers=[layer],
                tooltip={"text": "{name}"}
            )
        )
        # Обработчик для клика на точке
        selected_city = st.selectbox("Выберите город для перехода", options=df["name"])
        if selected_city:
            city_link = df.loc[df["name"] == selected_city, "link"].values[0]
        if st.button(f"Перейти к {selected_city}"):
            st.write(f"[Перейти на сайт {selected_city}]({city_link})")
    elif viz_type == "Average Income":
        # Гистограмма среднего дохода
        fig = px.bar(
            regions_data,
            x='Region',
            y='Average_Income',
            title='Average Income by Region',
            color='Average_Income',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig)
    else:  # Banking Infrastructure
        # Инфраструктура (банки и банкоматы)
        fig1 = px.scatter(
            regions_data,
            x='Bank_Branches',
            y='ATM_Count',
            size='Average_Income',
            color='Region',
            title='Banking Infrastructure'
        )
        st.plotly_chart(fig1)


def mini_game():
    st.title("💰 Financial IQ Challenge")
    
    # Initialize session state for game variables
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None

    # Quiz questions database
    questions = {
    "Personal Finance Basic": [
        {
            "question": "If you have 10,000 tenge and put it in a savings account with 5% annual interest, how much will you have after one year?",
            "options": ["10,500 tenge", "10,050 tenge", "11,000 tenge", "10,000 tenge"],
            "correct": 0,
            "explanation": "With 5% interest, you'll earn 500 tenge (10,000 × 0.05) in interest, making the total 10,500 tenge."
        },
        {
            "question": "What is the primary purpose of an emergency fund?",
            "options": [
                "To invest in stocks.",
                "To cover unexpected expenses.",
                "To pay off debt.",
                "To save for retirement."
            ],
            "correct": 1,
            "explanation": "An emergency fund is designed to cover unexpected expenses like medical bills or car repairs."
        },
        {
            "question": "What does APR stand for in personal finance?",
            "options": [
                "Annual Percentage Rate",
                "Annual Payment Rate",
                "Average Payment Rate",
                "Applied Percentage Rate"
            ],
            "correct": 0,
            "explanation": "APR stands for Annual Percentage Rate and represents the yearly interest generated by a sum that's charged to borrowers or paid to investors."
        },
        {
            "question": "Which of the following is a good practice for managing personal debt?",
            "options": [
                "Only making minimum payments on credit cards.",
                "Consolidating high-interest debts into a lower-interest loan.",
                "Ignoring debts until they go away.",
                "Taking out new loans to pay off old ones."
            ],
            "correct": 1,
            "explanation": "Consolidating high-interest debts into a lower-interest loan can help reduce overall interest payments and simplify repayment."
        },
        {
            "question": "'Net worth' is defined as:",
            "options": [
                "'Total assets minus total liabilities.'",
                "'Total income minus total expenses.'",
                "'Total savings plus investments.'",
                "'Total cash on hand.'"
            ],
            "correct": 0,
            "explanation": "'Net worth' is calculated by subtracting total liabilities from total assets, giving a clear picture of financial health."
        },
        {
            "question": "'Inflation' refers to:",
            "options": [
                "'The increase in prices of goods and services over time.'",
                "'The decrease in purchasing power of money over time.'",
                "'The rise in stock market prices.'",
                "'The stability of currency value.'"
            ],
            "correct": 0,
            "explanation": "'Inflation' indicates how much prices for goods and services rise over time, affecting purchasing power."
        },
        {
            "question": "'Diversification' in investing means:",
            "options": [
                "'Investing all your money in one stock.'",
                "'Spreading investments across various asset classes to reduce risk.'",
                "'Putting all your eggs in one basket.'",
                "'Chasing after high returns.'"
            ],
            "correct": 1,
            "explanation": "'Diversification' involves spreading investments across different asset classes to minimize risk."
        },
        {
            "question": "'What is net pay?'",
            "options": [
                "'The amount you earn before taxes are deducted.'",
                "'The amount you take home after taxes and deductions.'",
                "'Your total earnings including bonuses.'",
                "'Your salary before any deductions are applied.'"
            ],
            "correct": 1,
            "explanation": "'Net pay' is your take-home pay after all deductions like taxes and retirement contributions have been taken out."
        },
        {
            "question": "'Are contributions to a traditional 401(k) plan deducted from your salary before or after taxes?'",
            "options": [
                "'Before taxes'",
                "'After taxes'"
            ],
            "correct": 0,
            "explanation": "'Before taxes' means that contributions lower your taxable income for the year they are made."
        },
        {
            "question": "'What is compound interest?'",
            "options": [
                "'Interest calculated only on the principal amount.'",
                "'Interest calculated on the initial principal and also on the accumulated interest from previous periods.'",
                "'Interest that decreases over time.'",
                "'Interest that is paid out monthly.'"
            ],
            "correct": 1,
            "explanation": "'Compound interest' is calculated on the initial principal as well as on the accumulated interest from previous periods."
        },
    ],
    "Saving and Budgeting": [
    {
        "question": "What is the recommended savings rate for an emergency fund?",
        "options": ["1 month of expenses", "3-6 months of expenses", "12 months of expenses", "Just enough to cover bills"],
        "correct": 1,
        "explanation": "Financial experts recommend saving 3-6 months' worth of essential living expenses for emergencies."
    },
    {
        "question": "What does the 50/30/20 rule suggest?",
        "options": ["50% needs, 30% wants, 20% savings", "50% savings, 30% needs, 20% wants", "60% needs, 20% wants, 20% savings", "40% needs, 40% wants, 20% savings"],
        "correct": 0,
        "explanation": "The 50/30/20 rule allocates 50% of income to needs, 30% to wants, and 20% to savings."
    },
    {
        "question": "What is a fixed expense?",
        "options": ["An expense that varies each month", "An expense that remains constant each month", "An unexpected expense", "A discretionary expense"],
        "correct": 1,
        "explanation": "Fixed expenses are costs that do not change from month to month, such as rent or mortgage payments."
    },
    {
        "question": "How often should you review your budget?",
        "options": ["Once a year", "Monthly", "Every few years", "Never"],
        "correct": 1,
        "explanation": "It's important to review your budget monthly to track spending and make necessary adjustments."
    },
    {
        "question": "What is the purpose of a budget?",
        "options": ["To track income only", "To control spending and save money", "To increase debt", "To manage investments"],
        "correct": 1,
        "explanation": "A budget helps manage finances by controlling spending and ensuring savings goals are met."
    },
    {
        "question": "'Discretionary spending' refers to:",
        "options": ["Essential expenses like rent", "Non-essential expenses like entertainment", "Savings contributions", "Debt repayments"],
        "correct": 1,
        "explanation": "'Discretionary spending' includes non-essential purchases that can be adjusted based on financial goals."
    },
    {
        "question": "'Net income' is defined as:",
        "options": ["Gross income before taxes", "Income after taxes and deductions", "Total earnings including bonuses", "Total earnings before any deductions"],
        "correct": 1,
        "explanation": "'Net income' is the amount of money you take home after taxes and other deductions."
    },
    {
        "question": "'Emergency funds' should primarily be used for:",
        "options": ["Planned vacations", "$1000 purchases", "$500 purchases", "$2000 purchases"],
        "correct": 0,
        "explanation": "'Emergency funds' are meant for unexpected expenses like medical emergencies or car repairs."
    },
    {
        "question": "'Variable expenses' are best described as:",
        "options": ["Expenses that stay the same every month", 
                    "'Expenses that can change from month to month'", 
                    "'Expenses that are always predictable'", 
                    "'Expenses that are not necessary"],
        "correct": 1,
        "explanation": "'Variable expenses' fluctuate based on consumption or usage, such as groceries or utilities."
    },
    {
        "question": "'Budgeting apps' can help you:",
        "options": ["Track spending automatically", 
                    "'Increase debt'", 
                    "'Avoid saving'", 
                    "'Ignore financial goals"],
        "correct": 0,
        "explanation": "'Budgeting apps' can automate tracking your spending and help you stay within your budget."
    },
],
    "Credit and Loans": [
    {
        "question": "What does APR stand for?",
        "options": ["Annual Payment Rate", "Annual Percentage Rate", "Average Payment Rate", "Applied Percentage Rate"],
        "correct": 1,
        "explanation": "APR refers to the annual percentage rate charged for borrowing or earned through an investment."
    },
    {
        "question": "What is a credit score used for?",
        "options": ["To determine your income level", "To assess your creditworthiness", "To evaluate your employment status", "To check your savings account balance"],
        "correct": 1,
        "explanation": "A credit score indicates how likely you are to repay borrowed money based on your credit history."
    },
    {
        "question": "What is a secured loan?",
        "options": ["A loan with no collateral", "A loan backed by collateral", "A loan with a co-signer", "A loan with higher interest rates"],
        "correct": 1,
        "explanation": "A secured loan requires collateral which the lender can claim if the loan is not repaid."
    },
    {
        "question": "What is an unsecured loan?",
        "options": ["A loan with lower interest rates", "A loan without collateral", "A loan requiring a co-signer", "A guaranteed loan"],
        "correct": 1,
        "explanation": "Unsecured loans typically have higher interest rates because they do not require collateral."
    },
    {
        "question": "What happens if you miss a loan payment?",
        "options": ["You receive lower interest rates", "You incur late fees", "Your credit score improves", "You automatically enter into a repayment plan"],
        "correct": 1,
        "explanation": "Missing a loan payment often results in late fees being charged."
    },
    {
        "question": "What is a credit report?",
        "options": ["A summary of your financial history", "A list of your assets", "A record of your monthly expenses", "A report on your job history"],
        "correct": 0,
        "explanation": "A credit report provides a detailed account of your credit history and current credit status."
    },
    {
        "question": "Which type of loan typically has the highest interest rate?",
        "options": ["Mortgage", "Personal loan", "Auto loan", "Student loan"],
        "correct": 1,
        "explanation": "Personal loans usually have higher interest rates compared to secured loans like mortgages or auto loans."
    },
    {
        "question": "'Defaulting' on a loan means:",
        "options": ["Paying off the loan early", "'Failing to make required payments'", "'Refinancing the loan'", "'Transferring the loan to another lender'"],
        "correct": 1,
        "explanation": "'Defaulting' on a loan means failing to make required payments as agreed in the loan contract."
    },
    {
        "question": "'How can you improve your credit score?'",
        "options": ["By taking out more loans", "'By making payments on time'", "'By ignoring your debts'", "'By closing old accounts'"],
        "correct": 1,
        "explanation": "'Making payments on time consistently helps improve your credit score over time.'"
    },
    {
        "question": "'What is a co-signer?'",
        "options": ["Someone who takes out a loan with you", "'Someone who guarantees repayment of a loan'", "'Someone who pays off your debt'", "'Someone who provides collateral'"],
        "correct": 1,
        "explanation": "'A co-signer agrees to take responsibility for repaying a loan if the primary borrower fails to do so.'"
    }
],
    "Investing for Beginners": [
    {
        "question": "What is the primary goal of investing?",
        "options": ["To save money", "To earn returns on money over time", "To avoid taxes", "To spend money"],
        "correct": 1,
        "explanation": "The primary goal of investing is to earn returns on money over time through various investment vehicles."
    },
    {
        "question": "What is compound interest?",
        "options": ["Interest calculated only on the principal amount", "Interest calculated on both principal and accumulated interest", "Interest that decreases over time", "Interest paid monthly"],
        "correct": 1,
        "explanation": "Compound interest is calculated on both the principal amount and any previously earned interest."
    },
    {
        "question": "'Stocks' represent:",
        "options": ["Ownership in a company", "Debt owed by a company", "Real estate investments", "Cash equivalents"],
        "correct": 0,
        "explanation": "'Stocks' represent ownership in a company and entitle shareholders to part of the company’s profits."
    },
    {
        "question": "'Bonds' are considered what type of investment?",
        "options": ["Equity investments", "'Debt investments'", "'Cash investments'", "'Real estate investments'"],
        "correct": 1,
        "explanation": "'Bonds' are debt investments where an investor loans money to an entity for periodic interest payments."
    },
    {
        "question": "'Diversification' in investing means:",
        "options": ["Investing all funds in one asset class", "'Spreading investments across various asset classes'", "'Investing only in stocks'", "'Avoiding risk entirely"],
        "correct": 1,
        "explanation": "'Diversification' involves spreading investments across different asset classes to reduce risk."
    },
    {
        "question": "'What is an index fund?'",
        "options": ["A fund that invests in real estate", "'A mutual fund designed to track a specific market index'", "'A fund that invests only in bonds'", "'A fund with no management fees"],
        "correct": 1,
        "explanation": "'An index fund' aims to replicate the performance of a specific market index, such as the S&P 500."
    },
    {
        "question": "'Which investment strategy focuses on long-term growth?'",
        "options": ["Day trading", "'Buy-and-hold investing'", "'Market timing'", "'Speculative trading'"],
        "correct": 1,
        "explanation": "'Buy-and-hold investing' involves purchasing securities with the intention of holding them for an extended period."
    },
    {
        "question": "'What does it mean to “buy low, sell high”?'",
        "options": ["Buying at market peak", "'Purchasing assets when prices are low and selling when prices rise'", "'Investing only in high-risk stocks'", "'Selling all assets immediately when purchased'"],
        "correct": 1,
        "explanation": "'Buy low, sell high' means purchasing assets at lower prices and selling them when their value increases."
    },
    {
        "question": "'What is dollar-cost averaging?'",
        "options": ["Investing all funds at once", "'Investing fixed amounts regularly regardless of price fluctuations'", "'Only buying stocks during market downturns'", "'Selling all investments during market highs'"],
        "correct": 1,
        "explanation": "'Dollar-cost averaging' involves investing fixed amounts regularly, reducing the impact of volatility."
    },
    {
       "question":"What type of account allows tax-free growth for retirement savings?",
       "options":["Traditional IRA","Roth IRA","401(k)","Regular savings account"],
       "correct": 1,
       "explanation":"A Roth IRA allows contributions made with after-tax dollars, enabling tax-free growth on earnings."
   }
],
    "Retirement Planning": [
    {
        "question": "At what age can you start withdrawing from a traditional IRA without penalties?",
        "options": ["59½ years old", "62 years old", "65 years old", "70½ years old"],
        "correct": 0,
        "explanation": "You can start withdrawing from a traditional IRA without penalties at age 59½."
    },
    {
        "question": "What does '401(k)' refer to?",
        "options": ["A type of pension plan", "An employer-sponsored retirement savings plan", "A government retirement program", "An insurance policy"],
        "correct": 1,
        "explanation": "'401(k)' is an employer-sponsored retirement savings plan allowing employees to save pre-tax income."
    },
    {
        "question": "Which retirement account allows tax-free withdrawals in retirement?",
        "options": ["Traditional IRA", "Roth IRA", "401(k)", "Pension plan"],
        "correct": 1,
        "explanation": "'Roth IRA' allows tax-free withdrawals during retirement since contributions are made with after-tax dollars."
    },
    {
        "question": "How much should you aim to save for retirement as a general rule?",
        "options": ["10-15% of your income", "5-10% of your income", "15-20% of your income", "25-30% of your income"],
        "correct": 0,
        "explanation": "Financial advisors generally recommend saving at least 10-15% of your income for retirement."
    },
    {
        "question": "'What is Social Security?'",
        "options": ["A private pension plan", "Government-provided retirement benefits", "An investment account", "An insurance policy"],
        "correct": 1,
        "explanation": "'Social Security' provides government-provided retirement benefits based on earnings history."
    },
    {
        "question": "'What does 'vesting' mean in relation to employer-sponsored retirement plans?'",
        "options": ["The requirement to work for an employer for a certain number of years before gaining full access", 
                    "'The process of transferring funds from one account to another'", 
                    "'The ability to withdraw funds at any time'", 
                    "'The minimum age for withdrawal without penalties'"],
        "correct": 0,
        "explanation": "'Vesting' refers to earning full rights over employer contributions after meeting specific service requirements."
    },
    {
        "question": "'Which factor can affect how much you need to save for retirement?'",
        "options": ["Expected lifestyle in retirement", "Inflation rates", "Healthcare costs", "All of the above"],
        "correct": 3,
        "explanation": "'All of the above' factors can significantly impact how much you need to save for retirement."
    },
    {
        "question": "'When should you start planning for retirement?'",
        "options": ["At least five years before retiring", "'In your forties'", "'As soon as you start working'", "'Only when nearing retirement age'"],
        "correct": 2,
        "explanation": "'Starting early helps maximize compound growth potential on retirement savings.'"
    },
    {
        "question": "'What is an annuity?'",
        "options": ["A type of stock investment", "'A fixed sum paid regularly during retirement'", 
                    "'An insurance policy only'", "'A government bond'"],
        "correct": 1,
        "explanation": "'An annuity provides regular payments during retirement, often purchased through insurance companies.'"
    },
    {
        "question": "'How often should you review your retirement plan?'",
        "options": ["Once every five years", "'Annually or whenever there’s a major life change'", 
                    "'Only when nearing retirement age'", "'Never; it’s set once and forgotten'"],
        "correct": 1,
        "explanation": "'It’s essential to review your retirement plan annually or after significant life changes.'"
    }
],
    "Budgeting and Expense Management": [
    {
        "question": "What is the primary purpose of a budget?",
        "options": ["To track income only", "To control spending and save money", "To increase debt", "To manage investments"],
        "correct": 1,
        "explanation": "The primary purpose of a budget is to control spending and ensure that you are saving money effectively."
    },
    {
        "question": "What does the term 'fixed expenses' refer to?",
        "options": ["Expenses that vary each month", "Expenses that remain constant each month", "Unexpected expenses", "Discretionary spending"],
        "correct": 1,
        "explanation": "'Fixed expenses' are costs that do not change from month to month, such as rent or mortgage payments."
    },
    {
        "question": "What is a variable expense?",
        "options": ["An expense that stays the same every month", "An expense that can change from month to month", "A necessary expense", "An expense that is always predictable"],
        "correct": 1,
        "explanation": "'Variable expenses' fluctuate based on consumption or usage, such as groceries or utilities."
    },
    {
        "question": "'Discretionary spending' includes which of the following?",
        "options": ["Rent and utilities", "Groceries and basic necessities", "Dining out and entertainment", "Insurance premiums"],
        "correct": 2,
        "explanation": "'Discretionary spending' refers to non-essential expenses that can be adjusted based on financial goals."
    },
    {
        "question": "'What is the 50/30/20 rule?'",
        "options": ["50% needs, 30% wants, 20% savings", "50% savings, 30% needs, 20% wants", "60% needs, 20% wants, 20% savings", "40% needs, 40% wants, 20% savings"],
        "correct": 0,
        "explanation": "'The 50/30/20 rule' suggests allocating 50% of income to needs, 30% to wants, and 20% to savings."
    },
    {
        "question": "'What is an emergency fund?'",
        "options": ["A fund for planned vacations", "'A savings account for unexpected expenses'", "'A retirement account'", "'A fund for daily expenses"],
        "correct": 1,
        "explanation": "'An emergency fund' is a savings account set aside for unexpected expenses like medical emergencies or car repairs."
    },
    {
        "question": "'How often should you review your budget?'",
        "options": ["Once a year", "'Monthly'", "'Every few years'", "'Never"],
        "correct": 1,
        "explanation": "'Reviewing your budget monthly helps you track spending and make necessary adjustments.'"
    },
    {
        "question": "'What is the purpose of tracking your expenses?'",
        "options": ["To know where your money goes", "'To increase your spending'", "'To avoid budgeting altogether'", "'To reduce your income"],
        "correct": 0,
        "explanation": "'Tracking your expenses helps you understand your spending habits and identify areas for improvement.'"
    },
    {
        "question": "'What should you do if you overspend in one category of your budget?'",
        "options": ["Ignore it and hope it balances out next month", "'Adjust other categories to compensate'", "'Increase your income immediately'", "'Cut all discretionary spending"],
        "correct": 1,
        "explanation": "'Adjusting other categories allows you to stay within your overall budget while managing overspending.'"
    }
],
    "Insurance Fundamentals": [
    {
        "question": "What is the primary purpose of insurance?",
        "options": ["To provide investment returns", "To protect against financial loss", "To avoid paying taxes", "To increase savings"],
        "correct": 1,
        "explanation": "The primary purpose of insurance is to protect individuals and businesses from financial loss due to unforeseen events."
    },
    {
        "question": "What does 'premium' refer to in an insurance policy?",
        "options": ["The amount paid for coverage", "The deductible amount", "The payout amount", "The policy limit"],
        "correct": 0,
        "explanation": "'Premium' is the amount you pay for your insurance coverage, typically on a monthly or annual basis."
    },
    {
        "question": "'Deductible' is defined as:",
        "options": ["The total coverage amount", "'The amount you pay out of pocket before insurance kicks in'", 
                    "'The premium amount paid annually'", "'The maximum payout by the insurer"],
        "correct": 1,
        "explanation": "'Deductible' is the amount you must pay before your insurance company starts to pay for covered expenses."
    },
    {
        "question": "'What is a policy limit?'",
        "options": ["The maximum amount an insurer will pay for a covered loss", 
                    "'The minimum coverage required by law'", 
                    "'The total premium paid over the life of the policy'", 
                    "'The deductible amount"],
        "correct": 0,
        "explanation": "'Policy limit' refers to the maximum amount an insurer will pay for a covered loss as specified in the policy."
    },
    {
        "question": "'What type of insurance covers damage to your vehicle?'",
        "options": ["Health insurance", "'Auto insurance'", 
                    "'Homeowners insurance'", 
                    "'Life insurance'"],
        "correct": 1,
        "explanation": "'Auto insurance' provides coverage for damage to your vehicle as well as liability for damages to others."
    },
    {
        "question": "'What is life insurance designed to do?'",
        "options": ["Provide health coverage", 
                    "'Pay a benefit upon the insured's death'", 
                    "'Cover property damage'", 
                    "'Protect against liability"],
        "correct": 1,
        "explanation": "'Life insurance' pays a benefit to beneficiaries upon the insured person's death."
    },
    {
        "question": "'What does homeowners insurance typically cover?'",
        "options": ["Only the structure of the home", 
                    "'The structure, personal belongings, and liability protection'", 
                    "'Only personal belongings'", 
                    "'Only liability protection"],
        "correct": 1,
        "explanation": "'Homeowners insurance' usually covers the structure of the home, personal belongings, and liability protection."
    },
    {
        "question": "'What is liability insurance?'",
        "options": ["Insurance that covers your own injuries", 
                    "'Insurance that protects against claims from injuries or damages to others'", 
                    "'Insurance that covers property damage only'", 
                    "'Insurance that provides income replacement"],
        "correct": 1,
        "explanation": "'Liability insurance' protects you against claims resulting from injuries or damages to other people or their property."
    },
    {
        "question": "'What is a rider in an insurance policy?'",
        "options": ["A type of claim", 
                    "'An additional provision that modifies the original policy'", 
                    "'A higher premium payment'", 
                    "'A type of deductible"],
        "correct": 1,
        "explanation": "'A rider' is an additional provision added to an insurance policy that modifies its terms or coverage."
    },
    {
       "question":"What should you consider when choosing an insurance policy?",
       "options":["Coverage limits and deductibles","Premium costs","Insurer's reputation","All of the above"],
       "correct": 3,
       "explanation":"When choosing an insurance policy, it's important to consider coverage limits, deductibles, premium costs, and the insurer's reputation."
   }
],
    "Taxes and Tax Planning": [
    {
        "question": "What is the purpose of tax planning?",
        "options": ["To avoid paying taxes", "To minimize tax liability legally", "To increase taxable income", "To file taxes late"],
        "correct": 1,
        "explanation": "The purpose of tax planning is to minimize tax liability legally through various strategies."
    },
    {
        "question": "What is a tax deduction?",
        "options": ["An amount subtracted from your taxable income", "A flat fee paid to the IRS", "A percentage of your income taxed", "An extra charge on your tax return"],
        "correct": 0,
        "explanation": "A tax deduction reduces your taxable income, which can lower the amount of tax you owe."
    },
    {
        "question": "What is a tax credit?",
        "options": ["An amount that reduces your taxable income", "An amount subtracted directly from the taxes owed", "A fee paid for filing taxes", "A penalty for late filing"],
        "correct": 1,
        "explanation": "A tax credit directly reduces the amount of tax you owe, making it more valuable than a deduction."
    },
    {
        "question": "'What is the standard deduction?'",
        "options": ["A fixed dollar amount that reduces taxable income", 
                    "'An itemized deduction for specific expenses'", 
                    "'A credit for low-income earners'", 
                    "'A penalty for not filing taxes"],
        "correct": 0,
        "explanation": "'The standard deduction' is a fixed dollar amount that reduces your taxable income based on your filing status."
    },
    {
        "question": "'What is a W-2 form?'",
        "options": ["A form used to report self-employment income", 
                    "'A form used by employers to report wages paid to employees'", 
                    "'A form for reporting capital gains'," 
                    "'A form for reporting rental income"],
        "correct": 1,
        "explanation": "'The W-2 form' reports annual wages and the amount of taxes withheld from an employee's paycheck."
    },
    {
        "question": "What is capital gains tax?",
        "options": ["Tax on income earned from employment", 
                    "Tax on profits from the sale of assets or investments", 
                    "Tax on property ownership",
                    "Tax on sales transactions"],
        "correct": 1,
        "explanation": "'Capital gains tax' is levied on the profit made from selling an asset or investment."
    },
    {
        "question": "'Which of the following is considered taxable income?'",
        "options": ["Gifts received under $15,000", 
                    "'Wages earned from employment'", 
                    "'Inheritance received'", 
                    "'Child support payments"],
        "correct": 1,
        "explanation": "'Wages earned from employment' are considered taxable income and must be reported on your tax return."
    },
    {
        "question": "'What does it mean to itemize deductions?'",
        "options": ["To take the standard deduction instead", 
                    "'To list individual expenses that qualify for deductions'", 
                    "'To claim a flat rate deduction'", 
                    "'To apply for a tax credit"],
        "correct": 1,
        "explanation": "'Itemizing deductions' means listing individual eligible expenses on your tax return instead of taking the standard deduction."
    },
    {
    "question":"What is the deadline for filing individual income tax returns in the U.S.?",
    "options":["March 15","April 15","May 15","June 15"],
    "correct": 1,
    "explanation":"The deadline for filing individual income tax returns in the U.S. is typically April 15."
    },
    {
    "question":"What is a 1099 form used for?",
    "options":["Reporting wages paid to employees","Reporting self-employment income","Reporting capital gains","Reporting mortgage interest"],
    "correct": 1,
    "explanation":"The 1099 form is used to report various types of income other than wages, salaries, and tips, such as self-employment income."
    } 
]
}
    total_questions = len(questions["Personal Finance Basic"])
    # Start game screen
    if not st.session_state.game_started and not st.session_state.game_over:
        st.markdown("""
        ## Welcome to Financial IQ Challenge! 🎮
        
        Test your financial knowledge with this fun quiz game.
        
        ### Rules:
        - Answer 5 financial questions
        - Each correct answer gives you 100 points
        - Try to get the highest score possible!
        """)

        selected_topic = st.selectbox("Select topic", list(questions.keys()))
        if st.button("Start Game"):
            st.session_state.selected_topic = selected_topic
            st.session_state.game_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.rerun()

    # Game interface
    elif st.session_state.game_started and not st.session_state.game_over:
        # Retrieve questions from the selected topic
        topic_questions = questions[st.session_state.selected_topic]

        # Progress bar
        progress = (st.session_state.current_question + 1) / total_questions
        st.progress(progress)

        # Score display
        st.metric("Score", f"{st.session_state.score} points")

        # Current question
        current = topic_questions[st.session_state.current_question]

        # Question container
        with st.container():
            st.markdown(f"### Question {st.session_state.current_question + 1}:")
            st.markdown(f"**{current['question']}**")

            # Answer selection
            choice = st.radio(
                "Select your answer:",
                current["options"],
                key=f"q_{st.session_state.current_question}"
            )

            if st.button("Submit Answer"):
                # Check answer
                if choice == current["options"][current["correct"]]:
                    st.session_state.score += 100
                    st.success("Correct! 🎉")
                else:
                    st.error("Incorrect!")

                # Show explanation
                st.info(f"Explanation: {current['explanation']}")

                # Move to next question or end game
                if st.session_state.current_question < total_questions - 1:
                    st.session_state.current_question += 1
                else:
                    st.session_state.game_over = True

                st.rerun()

    # Game over screen
    elif st.session_state.game_over:
        st.balloons()

        # Display final score and message
        st.markdown(f"## Game Over! 🎮")
        st.markdown(f"### Final Score: {st.session_state.score} points")

        # Performance message
        if st.session_state.score == total_questions * 100:
            st.success("Perfect score! You're a financial genius! 🏆")
        elif st.session_state.score >= 300:
            st.success("Great job! You have solid financial knowledge! 🌟")
        else:
            st.info("Keep learning! Every financial master started somewhere! 📚")

        # Offer to play again
        if st.button("Play Again"):
            st.session_state.total_questions = 0
            st.session_state.score = 0
            st.session_state.current_question = 0
            st.session_state.game_started = False
            st.session_state.game_over = False
            st.rerun()

        # Display additional information
        st.markdown("""
        ### Fun Facts About Finance in Kazakhstan:
        - The national currency, Tenge, was introduced in 1993
        - Kazakhstan has a growing fintech sector
        - Financial literacy is a key focus in education reform
        """)

def expense_tracker():
    st.title("Expense Tracker")
    
    # Initialize session state for expenses if it doesn't exist
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame({
            'Date': [],
            'Category': [],
            'Amount': [],
            'Description': []
        })

    # Simple expense categories
    categories = [
        "Food",
        "Transport",
        "Education",
        "Entertainment",
        "Other"
    ]

    # Input form for new expenses
    st.subheader("Add New Expense")
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input("Date")
        category = st.selectbox("Category", categories)
    
    with col2:
        amount = st.number_input("Amount (KZT)", min_value=0)
        description = st.text_input("Description (Optional)")

    if st.button("Add Expense"):
        new_expense = pd.DataFrame({
            'Date': [date],
            'Category': [category],
            'Amount': [amount],
            'Description': [description]
        })
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
        st.success("✅ Expense added successfully!")

    # Display expenses if there are any
    if not st.session_state.expenses.empty:
        st.subheader("Your Expenses")
        
        # Summary metrics
        total_spent = st.session_state.expenses['Amount'].sum()
        st.markdown(f"### Total Spent: {total_spent:,.2f} KZT")

        # Show expenses table
        st.dataframe(
            st.session_state.expenses.sort_values('Date', ascending=False),
            hide_index=True,
            column_order=['Date', 'Category', 'Amount', 'Description']
        )

        # Simple visualization
        st.subheader("Expenses by Category")
        fig = px.pie(
            st.session_state.expenses,
            values='Amount',
            names='Category',
            title='Expense Distribution'
        )
        st.plotly_chart(fig)

        # Download options
        if st.button("Download Data as CSV"):
            csv = st.session_state.expenses.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="expenses.csv",
                mime="text/csv"
            )
            
        # Clear data option
        if st.button("Clear All Data"):
            st.session_state.expenses = pd.DataFrame({
                'Date': [],
                'Category': [],
                'Amount': [],
                'Description': []
            })
            st.success("All data cleared!")

# ~~ Gemini Content Generation Function ~~
# pip install google-generativeai
def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# --- ChatBot Streamlit App ---
def gemini_chatbot():
    # Streamed response emulator
    def response_generator(prompt):
        response = get_ai_response(prompt)
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def chat_bot():
    st.title("💸 Financial Assistant Chatbot")
    st.write("Ask me anything about personal finance, budgeting, or investment strategies!")
    gemini_chatbot()
