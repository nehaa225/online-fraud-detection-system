import re

URGENT_KEYWORDS = ['urgent', 'immediate', 'suspend', 'blocked', 'expire', 'warning', 'important', 'action required']
MONEY_KEYWORDS = ['win', 'prize', 'money', 'cash', 'transfer', 'bitcoin', 'investment', '$', 'fee', 'paypal', 'bank']
LINK_PATTERN = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def analyze_risk(text):
    score = 0
    patterns_found = []
    
    text_lower = text.lower()
    
    for kw in URGENT_KEYWORDS:
        if kw in text_lower:
            score += 25
            patterns_found.append(f"Urgency keyword detected ('{kw}')")
            break
            
    for kw in MONEY_KEYWORDS:
        if kw in text_lower:
            score += 25
            patterns_found.append(f"Financial/Reward keyword detected ('{kw}')")
            break
            
    urls = re.findall(LINK_PATTERN, text)
    if urls:
        score += 30
        patterns_found.append("URL/Link detected")
        
    if 'otp' in text_lower or 'password' in text_lower or 'ssn' in text_lower or 'kyc' in text_lower:
        score += 30
        patterns_found.append("Request for sensitive information (OTP/Password/KYC)")
        
    score = min(score, 100)
    
    if score >= 70:
        level = "High"
        suggestion = "🚨 High Risk! Do NOT click any links, do NOT share personal info. Contact the official institution directly."
    elif score >= 40:
        level = "Medium"
        suggestion = "⚠️ Medium Risk! Proceed with caution. Verify the sender's identity before taking any action."
    else:
        level = "Low"
        suggestion = "✅ Low Risk. Seems safe, but always remain vigilant."
        
    if not patterns_found:
        patterns_found.append("No immediate suspicious patterns detected.")
        
    return score, level, patterns_found, suggestion
