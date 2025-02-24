import smtplib
import socket
from config import SMTP_PORTS
from ip_rotation import get_next_ip, mark_ip_blacklisted, update_ip_usage
from utils import is_valid_email, has_valid_mx_record

def verify_email(email):
    """Verify an email by checking MX records and performing SMTP validation."""
    domain = email.split('@')[1]

    if not has_valid_mx_record(domain):
        return False

    selected_ip = get_next_ip()
    if not selected_ip:
        return False  # No working IP available

    original_socket = socket.socket
    socket.socket = lambda *args, **kwargs: original_socket(*args, **kwargs)
    socket.getaddrinfo = lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (selected_ip, 0))]

    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mail_server = str(mx_records[0].exchange)

        for port in SMTP_PORTS:
            try:
                if port == 465:
                    smtp = smtplib.SMTP_SSL(mail_server, port, timeout=10)
                else:
                    smtp = smtplib.SMTP(mail_server, port, timeout=10)

                smtp.ehlo()
                smtp.quit()

                update_ip_usage(selected_ip)
                return True
            except:
                continue

        mark_ip_blacklisted(selected_ip)
        return False

    except:
        return False
