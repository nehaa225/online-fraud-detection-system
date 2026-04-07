import streamlit as st
import database
import fraud_model
import risk_analysis
import url_checker
import voice_detection
import quiz
import alerts
import importlib
importlib.reload(alerts)
import pytesseract
import time

SESSION_TIMEOUT_SECONDS = 300 # 5 minutes

from PIL import Image
import os
import io

# Optional: Set tesseract path to local install if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="FraudShield AI", page_icon="🛡️", layout="wide")

import base64

def inject_bg(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background: linear-gradient(rgba(10, 14, 23, 0.8), rgba(10, 14, 23, 0.95)), 
                                url(data:image/png;base64,{encoded_string});
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
    except Exception as e:
        pass

def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        .stApp {
            font-family: 'Outfit', sans-serif;
            color: #f8fafc;
        }
        
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.6) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(139, 92, 246, 0.2);
        }

        .main-header {
            background: linear-gradient(90deg, #c084fc 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem !important;
            font-weight: 800;
            text-align: center;
            letter-spacing: -1px;
            margin-bottom: 2rem;
            text-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
        }
        
        .subheader {
            color: #a78bfa;
            font-weight: 600;
        }
        
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, textarea {
            background-color: rgba(30, 41, 59, 0.5) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(139, 92, 246, 0.3) !important;
            color: white !important;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
            width: 100%;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
            box-shadow: 0 0 25px rgba(139, 92, 246, 0.6);
            transform: translateY(-2px);
            color: white;
            border: none;
        }
        
        .glass-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2);
            border: 1px solid rgba(139, 92, 246, 0.4);
        }
        
        .glass-card h3 {
            color: #a78bfa;
            border-bottom: 1px solid rgba(139,92,246,0.3);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        .glass-card ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .glass-card ul li {
            padding: 10px 0;
            color: #cbd5e1;
            border-bottom: 1px dashed rgba(255,255,255,0.1);
        }
        
        .glass-card ul li:last-child {
            border-bottom: none;
        }
        
        .glass-card ul li b {
            color: #60a5fa;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# Initialize DB
database.create_tables()

# Session State for Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'role' not in st.session_state:
    st.session_state['role'] = ''
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

import random

def login_register_page():
    inject_bg(r"C:\Users\DELL\.gemini\antigravity\brain\36e9f5cc-ec3f-4653-83bf-963bee7cb0cd\auth_bg_1775567445553.png")
    st.markdown("<h1 class='main-header'>🛡️ FraudShield AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 2rem; color: #cbd5e1;'>Your personal digital guardian against online scams.</h3>", unsafe_allow_html=True)
    
    if 'auth_view' not in st.session_state:
        st.session_state['auth_view'] = 'login'
    if 'otp_code' not in st.session_state:
        st.session_state['otp_code'] = None 
    if 'pending_user' not in st.session_state:
        st.session_state['pending_user'] = None
        
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state['auth_view'] == 'login':
            st.subheader("Login to your account")
            log_user = st.text_input("Username", key="log_user")
            log_pass = st.text_input("Password", type="password", key="log_pass")
            if st.button("Login", use_container_width=True):
                user = database.login_user(log_user, log_pass)
                if user:
                    email = user['email'] if 'email' in user.keys() else None
                    if not email or user['username'] == 'admin':
                        st.session_state['logged_in'] = True
                        st.session_state['user_id'] = user['id']
                        st.session_state['username'] = user['username']
                        st.session_state['role'] = user['role']
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        otp = str(random.randint(100000, 999999))
                        st.session_state['otp_code'] = otp
                        st.session_state['pending_user'] = user
                        
                        success, error = alerts.send_otp(email, otp)
                        if success:
                            st.session_state['auth_view'] = 'verify_login'
                            st.success(f"OTP sent to {email}")
                            st.rerun()
                        else:
                            st.error(f"Failed to send OTP. Check console/alerts.py. Error: {error}")
                else:
                    st.error("Invalid username or password.")
                    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Don't have an account?")
            if st.button("Register Here", use_container_width=True):
                st.session_state['auth_view'] = 'register'
                st.rerun()
                
        elif st.session_state['auth_view'] == 'verify_login':
            st.subheader("Enter OTP")
            st.info("Check your email for the 6-digit authentication code.")
            otp_input = st.text_input("OTP Code", key="login_otp")
            if st.button("Verify & Login", use_container_width=True):
                if otp_input == st.session_state['otp_code']:
                    user = st.session_state['pending_user']
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user['id']
                    st.session_state['username'] = user['username']
                    st.session_state['role'] = user['role']
                    st.session_state['otp_code'] = None
                    st.session_state['pending_user'] = None
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid OTP Code.")
            
            if st.button("Back to Login", use_container_width=True):
                st.session_state['auth_view'] = 'login'
                st.rerun()

        elif st.session_state['auth_view'] == 'register':
            st.subheader("Create an account")
            reg_user = st.text_input("New Username", key="reg_user")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_pass = st.text_input("New Password", type="password", key="reg_pass")
            reg_role = st.selectbox("Role", ["User", "Admin"])
            if st.button("Register & Send OTP", use_container_width=True):
                if reg_user and reg_pass and reg_email:
                    otp = str(random.randint(100000, 999999))
                    st.session_state['otp_code'] = otp
                    st.session_state['pending_user'] = {
                        "user": reg_user,
                        "email": reg_email,
                        "pass": reg_pass,
                        "role": reg_role
                    }
                    success, error = alerts.send_otp(reg_email, otp)
                    if success:
                        st.session_state['auth_view'] = 'verify_register'
                        st.success(f"OTP sent to {reg_email}")
                        st.rerun()
                    else:
                        st.error(f"Failed to send OTP email: {error}")
                else:
                    st.error("Please fill all fields, including email.")
                    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Already have an account?")
            if st.button("Login Here", use_container_width=True):
                st.session_state['auth_view'] = 'login'
                st.rerun()

        elif st.session_state['auth_view'] == 'verify_register':
            st.subheader("Verify Email")
            st.info("Check your email for the 6-digit authentication code.")
            otp_input = st.text_input("OTP Code", key="reg_otp")
            if st.button("Verify & Complete Registration", use_container_width=True):
                if otp_input == st.session_state['otp_code']:
                    pending = st.session_state['pending_user']
                    success = database.add_user(pending['user'], pending['email'], pending['pass'], pending['role'])
                    if success:
                        st.success("Registration successful! Please login.")
                        st.session_state['auth_view'] = 'login'
                        st.session_state['otp_code'] = None
                        st.session_state['pending_user'] = None
                        st.rerun()
                    else:
                        st.error("Username already exists or database error.")
                else:
                    st.error("Invalid OTP Code.")
                    
            if st.button("Back to Register", use_container_width=True):
                st.session_state['auth_view'] = 'register'
                st.rerun()

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = ''
    st.session_state['role'] = ''

def analyze_and_report_ui(text, scan_type):
    st.markdown("### 🤖 Analysis Results")
    prediction, confidence = fraud_model.predict_fraud(text)
    
    score, level, patterns, suggestion = risk_analysis.analyze_risk(text)
    
    # UI Presentation
    col1, col2 = st.columns(2)
    with col1:
        if prediction == "Fraud":
            st.error(f"**AI Prediction:** {prediction} ({confidence:.2f}% Confidence)")
        else:
            st.success(f"**AI Prediction:** {prediction} ({confidence:.2f}% Confidence)")
            
    with col2:
        if level == "High":
            st.error(f"**Risk Score:** {score}% ({level})")
        elif level == "Medium":
            st.warning(f"**Risk Score:** {score}% ({level})")
        else:
            st.success(f"**Risk Score:** {score}% ({level})")
            
    st.markdown("#### 🔍 Detected Patterns")
    for p in patterns:
        st.markdown(f"- {p}")
        
    st.markdown("#### 💡 Recommendation")
    st.info(suggestion)
    
    # Save Report
    if st.button("Report to Database"):
        database.add_report(st.session_state['user_id'], scan_type, text, "")
        st.success("Successfully reported!")

def app_main():
    inject_bg(r"C:\Users\DELL\.gemini\antigravity\brain\36e9f5cc-ec3f-4653-83bf-963bee7cb0cd\hero_bg_1775567462979.png")
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {st.session_state['username']}")
        st.markdown(f"**Role:** {st.session_state['role']}")
        st.button("Logout", on_click=logout)
        st.divider()
        
        if st.session_state['role'] == 'Admin':
            menu = ["Dashboard", "Admin Panel"]
        else:
            menu = ["Dashboard", "Report a Scam", "Text Detection", "URL Checker", "Image OCR", "Voice Scan", "Cyber Quiz"]
            
        choice = st.radio("Navigation", menu)
        
    if choice == "Dashboard":
        st.markdown("<h1 class='main-header'>Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("Welcome to FraudShield AI. Select a module from the sidebar to begin analyzing potentially fraudulent content.")
        
        st.markdown("""
        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 2rem;">
            <div class="glass-card" style="flex: 1; min-width: 300px;">
                <h3>📝 Text Detection</h3>
                <p style="color: #cbd5e1;">Paste suspicious emails or messages to check for fraud using Machine Learning.</p>
            </div>
            <div class="glass-card" style="flex: 1; min-width: 300px;">
                <h3>🌐 URL Checker</h3>
                <p style="color: #cbd5e1;">Verify if a link is safe before clicking to prevent phishing attacks.</p>
            </div>
            <div class="glass-card" style="flex: 1; min-width: 300px;">
                <h3>📸 Image OCR</h3>
                <p style="color: #cbd5e1;">Extract and analyze text directly from screenshots of malicious messages.</p>
            </div>
            <div class="glass-card" style="flex: 1; min-width: 300px;">
                <h3>🎤 Voice Scan</h3>
                <p style="color: #cbd5e1;">Upload audio clips or voicemails to heavily scrutinize for AI deepfakes and fraudulent patterns.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif choice == "Report a Scam":
        st.markdown("<h1 class='main-header'>🚨 Report a Scam</h1>", unsafe_allow_html=True)
        st.info("Have you encountered a scam online? Report it here to help awareness.")
        
        with st.form("manual_report_form"):
            report_type = st.selectbox("Type of Scam", ["Email/Phishing", "Fake URL/Website", "Social Media/Impersonation", "Phone Call/SMS", "Other"])
            report_desc = st.text_area("Description of the Scam")
            report_link = st.text_input("Related Link/URL (Optional)")
            
            submitted = st.form_submit_button("Submit Report")
            if submitted:
                if report_desc:
                    database.add_report(st.session_state['user_id'], report_type, report_desc, report_link)
                    st.success("Thank you! Your report has been submitted successfully and sent to administrators.")
                else:
                    st.error("Please provide a description of the scam before submitting.")
                    
    elif choice == "Text Detection":
        st.markdown("<h1 class='main-header'>📝 Text Fraud Detection</h1>", unsafe_allow_html=True)
        msg = st.text_area("Paste the message or email content here:")
        if st.button("Analyze Text"):
            if msg:
                analyze_and_report_ui(msg, "Text")
            else:
                st.warning("Please enter some text.")
                
    elif choice == "URL Checker":
        st.markdown("<h1 class='main-header'>🔗 URL Checker</h1>", unsafe_allow_html=True)
        url = st.text_input("Enter URL (e.g., http://example.com):")
        if st.button("Check URL"):
            if url:
                is_suspicious, reasons = url_checker.check_url(url)
                if is_suspicious:
                    st.error("🚨 Suspicious URL Detected!")
                    for r in reasons:
                        st.markdown(f"- {r}")
                    database.add_report(st.session_state['user_id'], "URL", "Suspicious link detected", url)
                else:
                    st.success("✅ URL appears to be structurally safe.")
                    for r in reasons:
                        st.markdown(f"- {r}")
            else:
                st.warning("Please enter a URL.")
                
    elif choice == "Image OCR":
        st.markdown("<h1 class='main-header'>📸 Screenshot Analysis</h1>", unsafe_allow_html=True)
        st.info("Upload a screenshot of a suspicious message.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_container_width=True)
            
            if st.button("Extract and Analyze Text"):
                with st.spinner("Extracting text via OCR..."):
                    try:
                        extracted_text = pytesseract.image_to_string(image)
                        st.text_area("Extracted Text:", extracted_text, height=150)
                        
                        if extracted_text.strip():
                            analyze_and_report_ui(extracted_text, "Image (OCR)")
                        else:
                            st.warning("No text found in the image.")
                    except Exception as e:
                        st.error(f"OCR Error: Ensure Tesseract is installed. {e}")
                        
    elif choice == "Voice Scan":
        st.markdown("<h1 class='main-header'>🎤 Voice AI Detection</h1>", unsafe_allow_html=True)
        st.info("Upload a suspicious voicemail or call recording (.wav, .mp3, .mp4, .mpeg).")
        audio_file = st.file_uploader("Choose an audio/video file...", type=["wav", "mp3", "mp4", "mpeg"])
        
        if audio_file is not None:
            # We can't always natively play all formats cleanly via st.audio, but Streamlit passes most generic formats through to the browser.
            st.audio(audio_file)
            
            if st.button("Transcribe and Analyze"):
                with st.spinner("Transcribing..."):
                    success, result = voice_detection.extract_text_from_audio(audio_file)
                    if success:
                        st.text_area("Transcription:", result, height=150)
                        analyze_and_report_ui(result, "Voice Audio")
                    else:
                        st.error(result)
                        
    elif choice == "Cyber Quiz":
        st.markdown("<h1 class='main-header'>🧠 Cyber Awareness Quiz</h1>", unsafe_allow_html=True)
        
        if "quiz_score" not in st.session_state:
            st.session_state.quiz_score = 0
            st.session_state.quiz_submitted = False
            
        questions = quiz.QUESTIONS
        
        with st.form("quiz_form"):
            user_answers = []
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                ans = st.radio("Select an option:", q['options'], key=f"q_{i}", index=None)
                user_answers.append(ans)
                st.markdown("---")
                
            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                score = 0
                st.session_state.quiz_submitted = True
                
                # Check answers within form context 
                # (but we can display results outside or via rerender)
                st.session_state.user_answers = user_answers

        if st.session_state.get('quiz_submitted'):
            st.markdown("### Results:")
            score = 0
            for i, q in enumerate(questions):
                selected = st.session_state.user_answers[i]
                correct_ans = q['options'][q['answer']]
                
                st.markdown(f"**Q{i+1}:** {q['question']}")
                if selected == correct_ans:
                    st.success("Correct!")
                    score += 1
                else:
                    st.error(f"Incorrect. The correct answer was: {correct_ans}")
                st.info(f"Explanation: {q['explanation']}")
                
            st.metric(label="Final Score", value=f"{score} / {len(questions)}")
            
            if st.button("Retake Quiz"):
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = []
                st.rerun()
                
    elif choice == "Admin Panel":
        st.markdown("<h1 class='main-header'>👨‍💼 Admin Dashboard</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["User Management", "Fraud Reports"])
        
        with tab1:
            st.subheader("Registered Users")
            users = database.get_all_users()
            for u in users:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**ID:** `{u['id']}` - **Username:** `{u['username']}` - **Role:** `{u['role']}`")
                with col2:
                    if u['username'] != 'admin':
                        if st.button("Remove", key=f"del_{u['id']}", use_container_width=True):
                            database.remove_user(u['id'])
                            st.success(f"User {u['username']} removed!")
                            st.rerun()
                
        with tab2:
            st.subheader("Global Fraud Reports")
            reports = database.get_all_reports()
            
            if not reports:
                st.info("No reports submitted yet.")
                
            for r in reports:
                st.markdown(f"""
                <div class="glass-card">
                    <b>Reporter:</b> {r['username']}<br>
                    <b>Time:</b> {r['timestamp']}<br>
                    <b>Type:</b> {r['type']}<br>
                    <b>Link:</b> {r['link']}<br>
                    <b>Description:</b> {r['description']}
                </div>
                """, unsafe_allow_html=True)

if 'last_activity' not in st.session_state:
    st.session_state['last_activity'] = time.time()
if 'session_expired' not in st.session_state:
    st.session_state['session_expired'] = False

if st.session_state.get('logged_in'):
    current_time = time.time()
    if current_time - st.session_state['last_activity'] > SESSION_TIMEOUT_SECONDS:
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = None
        st.session_state['username'] = ''
        st.session_state['role'] = ''
        st.session_state['auth_view'] = 'login'
        st.session_state['session_expired'] = True
        st.rerun()
    else:
        st.session_state['last_activity'] = current_time

if not st.session_state['logged_in']:
    login_register_page()
    if st.session_state.get('session_expired'):
        st.warning("Your session has expired due to inactivity. Please log in again.")
        st.session_state['session_expired'] = False
else:
    app_main()
