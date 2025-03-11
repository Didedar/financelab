import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
import yfinance as yf
from datetime import datetime
from modules.app import show_payment_modal, education_hub, interactive_maps, mini_game, expense_tracker, chat_bot
import json
import random
import time
import re

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('financelab.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY, 
                password TEXT, 
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# --- Authentication Functions ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def register_user(username, password, email):
    if not username or not password or not email:
        return False, "All fields are required"
    
    if not is_valid_email(email):
        return False, "Invalid email format"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    try:
        conn = sqlite3.connect('financelab.db')
        c = conn.cursor()
        
        # Check if username exists
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        if c.fetchone() is not None:
            conn.close()
            return False, "Username already exists"
        
        # Check if email exists
        c.execute("SELECT email FROM users WHERE email=?", (email,))
        if c.fetchone() is not None:
            conn.close()
            return False, "Email already registered"
        
        # Insert new user
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, hash_password(password), email))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
        
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def login_user(username, password):
    conn = sqlite3.connect('financelab.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

# --- Config and Style ---
st.set_page_config(page_title="FinanceLab", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-green { color: #72BF78; }
    .secondary-green { color: #A0D683; }
    .light-green { color: #D3EE98; }
    .yellow { color: #FEFF9F; }
    
    .sidebar { background-color: #f0f2f6; padding: 20px; }
    .buy-button {
        background-color: #72BF78;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
    }
    .auth-form {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .form-header {
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False


# --- Get current currencies ---
@st.cache_data 
def get_currencies(currencies):
    usd_to_kzt_ticker = yf.Ticker('KZT=X')
    usd_to_kzt_data = usd_to_kzt_ticker.history(period='1d')
    usd_to_kzt = usd_to_kzt_data['Close'].iloc[-1] 
    ounce_to_gram = 28.34952

    item_to_kzt = dict()

    for currency in currencies:
        ticker = yf.Ticker(currency)
        data = ticker.history(period='1d')
        if not data.empty:
            close_value = data['Close'].iloc[-1]
            if currency == 'BTC-USD':
                item_to_kzt[currency] = close_value * usd_to_kzt
            elif currency == 'GC=F':
                item_to_kzt[currency] = round(close_value * usd_to_kzt / ounce_to_gram, 2)
            else:
                item_to_kzt[currency] = close_value
        
    return item_to_kzt

# --- Sidebar ---
def sidebar():
    with st.sidebar:
        image_path = "Remove-bg.ai_1731141237249.png"

        # Загрузка изображения на sidebar
        st.sidebar.image(image_path, use_container_width=True)

        st.sidebar.markdown(
    """
    <p style='font-size:20px; font-weight:bold; text-align: center; margin-top: -50px;'> FinanceLab </p> """, unsafe_allow_html=True)
        
        # Market Data
        st.subheader("Market Data")

        currencies = ['KZT=X', 'EURKZT=X', 'BTC-USD', 'GC=F'] 

        item_to_kzt = get_currencies(currencies)

        for currency in currencies:
            if currency == 'BTC-USD':
                st.write(f"Bitcoin 💰: {item_to_kzt[currency]:.2f} KZT")
            elif currency == 'GC=F':
                st.write(f"Gold 🥇: {item_to_kzt[currency]:.2f} KZT")
            elif currency == 'KZT=X':
                st.write(f"Dollar 💲: {item_to_kzt[currency]:.2f} KZT")
            else:
                st.write(f"Euro 💶: {item_to_kzt[currency]:.2f} KZT")
        
        # Review Link
        st.markdown("[Leave a Review](https://forms.gle/H4J9pw5zERpX7jHr6Ыы)")
        

# --- Login/Register Page ---
def login_register_page():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        if not st.session_state.show_register:
            st.markdown("<div class='auth-form'>", unsafe_allow_html=True)
            st.markdown("<h2 class='form-header'>Login to FinanceLab</h2>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", use_container_width=True):
                    if login_user(username, password):
                        st.session_state.logged_in = True
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            with col2:
                if st.button("Register Instead", use_container_width=True):
                    st.session_state.show_register = True
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        else:
            st.markdown("<div class='auth-form'>", unsafe_allow_html=True)
            st.markdown("<h2 class='form-header'>Register for FinanceLab</h2>", unsafe_allow_html=True)
            
            reg_username = st.text_input("Username")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            reg_password_confirm = st.text_input("Confirm Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Register", use_container_width=True):
                    if reg_password != reg_password_confirm:
                        st.error("Passwords do not match")
                    else:
                        success, message = register_user(reg_username, reg_password, reg_email)
                        if success:
                            st.success(message)
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error(message)
            
            with col2:
                if st.button("Back to Login", use_container_width=True):
                    st.session_state.show_register = False
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)


# --- Landing Page ---
def landing_page():
    st.title("FinanceLab - Financial Literacy for Students")

    st.subheader("What awaits you?")
    st.markdown("""
        - Financial literacy lessons: Simple and easy-to-understand education.
        - Personal mentor: A virtual character will help you make financial decisions.
        - Practical tasks: Real-life situations to reinforce your knowledge.
        - Step by step: A clear approach starting from the basics.
                """)
    
    st.video('https://youtu.be/I9zzsILbgHo?si=ZgULbY_8ODbd3wcG')
    
    st.header("Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📚 Interactive Learning")
        st.write("Engaging lessons with videos and quizzes")
    with col2:
        st.markdown("### 🎮 Mini Games")
        st.write("Learn through play with financial games")
    with col3:
        st.markdown("### 📊 Expense Tracking")
        st.write("Track and analyze your spending")
    
    st.header("Pricing Plans")
    pricing_col1, pricing_col2 = st.columns(2)
    with pricing_col1:
        st.markdown("### Monthly Plan")
        st.markdown("$5/month")
        if st.button("Buy Monthly"):
            show_payment_modal("monthly")
    with pricing_col2:
        st.markdown("### Yearly Plan")
        st.markdown("$50/year")
        if st.button("Buy Yearly"):
            show_payment_modal("yearly")
    
    st.header("FAQ")
    with st.expander("What age is this suitable for?"):
        st.write("FinanceLab is designed for students aged 12-18.")
    
    st.markdown("""<iframe width="100%" height="450" frameborder="0" style="border:0" src="https://www.google.com/maps/embed?pb=YOUR-EMBED-URL" allowfullscreen></iframe>""", unsafe_allow_html=True)

# --- Main App Logic ---
def main():
    init_db()
    sidebar()
    
    if not st.session_state.logged_in:
        login_register_page()
        return
    
    pages = {
        "Home": landing_page,
        "Education Hub": education_hub,
        "Interactive Maps": interactive_maps,
        "Mini Game": mini_game,
        "Expense Tracker": expense_tracker,
        "Financial Assistant Bot": chat_bot
    }
    
    page = st.sidebar.selectbox("Navigate", list(pages.keys()))
    
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    pages[page]()

if __name__ == "__main__":
    main()
    # Footer
    st.markdown('''
    <style>
    .footer {
        background-color: #000B58;
    }
    </style>
''', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="footer"></div>', unsafe_allow_html=True)
    st.markdown("Created by FinanceLab Team")
    st.markdown("© 2024 All rights reserved")