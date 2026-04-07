import re

SUSPICIOUS_DOMAINS = ['login', 'update', 'secure', 'verify', 'account', 'free']

def check_url(url):
    reasons = []
    is_suspicious = False
    
    ip_pattern = r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'
    domain = url.split('//')[-1].split('/')[0]
    
    if re.match(ip_pattern, domain):
        reasons.append("URL uses an IP address instead of a domain name.")
        is_suspicious = True
        
    parts = domain.split('.')
    if len(parts) > 3 and parts[-1] not in ['uk', 'au', 'in', 'br']:
        reasons.append(f"URL has too many subdomains ({len(parts)}).")
        is_suspicious = True
        
    for kw in SUSPICIOUS_DOMAINS:
        if kw in domain.lower():
            reasons.append(f"URL contains suspicious keyword in domain: '{kw}'")
            is_suspicious = True
            
    if url.startswith('http://'):
        reasons.append("URL uses insecure HTTP connection.")
        is_suspicious = True
        
    if not is_suspicious:
        reasons.append("No immediate red flags detected for this URL.")
        
    return is_suspicious, reasons
