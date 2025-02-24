import random
from config import HOSTWINDS_IPS, MAX_EMAILS_PER_IP

BLACKLISTED_IPS = set()  # Store blacklisted IPs
IP_USAGE_COUNT = {}  # Track how many emails each IP has verified

def get_next_ip():
    """Select a working IP for rotation and discard blacklisted IPs."""
    available_ips = [ip for ip in HOSTWINDS_IPS if ip not in BLACKLISTED_IPS]
    
    if not available_ips:
        print("❌ All IPs are blacklisted! No working IP available.")
        return None
    
    # Rotate IPs using round-robin
    selected_ip = random.choice(available_ips)
    
    # Enforce IP warmup (prevent overuse)
    if IP_USAGE_COUNT.get(selected_ip, 0) >= MAX_EMAILS_PER_IP:
        print(f"⚠ IP {selected_ip} reached warmup limit. Rotating...")
        BLACKLISTED_IPS.add(selected_ip)
        return get_next_ip()  # Select another IP
    
    return selected_ip

def mark_ip_blacklisted(ip):
    """Mark an IP as blacklisted if SMTP fails."""
    BLACKLISTED_IPS.add(ip)
    print(f"⚠ IP {ip} has been blacklisted due to failed SMTP connections.")

def update_ip_usage(ip):
    """Increase usage count for an IP."""
    IP_USAGE_COUNT[ip] = IP_USAGE_COUNT.get(ip, 0) + 1
