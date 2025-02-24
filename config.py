# ==============================
# 📌 Hostwinds SMTP & IP Rotation
# ==============================

# List of Hostwinds IPs for rotation
HOSTWINDS_IPS = [
    "23.254.231.36",
    "192.236.160.29",
    "23.254.230.136",
    "192.119.111.15",
    "192.119.111.9",
    "192.119.110.49",
]

# Max emails per IP (for warmup)
MAX_EMAILS_PER_IP = 100

# SMTP Ports to check
SMTP_PORTS = [25, 587, 465]
