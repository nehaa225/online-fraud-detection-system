import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "nehaareddy02@gmail.com"
SMTP_PASSWORD = "klcw sist almi tgqx"

def send_alert(recipient_email, risk_level, description):
    if SMTP_USER == "your_email@gmail.com":
        return False, "SMTP server not configured. Please update alerts.py with valid credentials."
        
    msg = EmailMessage()
    msg.set_content(f"Alert!\n\nA {risk_level} risk activity was detected on your account.\n\nDescription:\n{description}\n\nPlease take appropriate action to secure your account.")
    
    msg['Subject'] = f"Security Alert: {risk_level} Risk Detected"
    msg['From'] = SMTP_USER
    msg['To'] = recipient_email
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, "Alert sent successfully!"
    except Exception as e:
        return False, str(e)

def send_otp(recipient_email, otp_code):
    if SMTP_USER == "your_email@gmail.com":
        print(f"SMTP not configured. Generated OTP for {recipient_email}: {otp_code}")
        return True, "SMTP not configured. Check console."
        
    msg = EmailMessage()
    msg.set_content(f"Your FraudShield AI Authentication Code is:\n\n{otp_code}\n\nDo not share this code with anyone.")
    
    msg['Subject'] = "FraudShield AI - Your OTP Code"
    msg['From'] = SMTP_USER
    msg['To'] = recipient_email
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, "OTP sent successfully!"
    except Exception as e:
        print(f"Email Error. Generated OTP for {recipient_email}: {otp_code}")
        return False, str(e)
