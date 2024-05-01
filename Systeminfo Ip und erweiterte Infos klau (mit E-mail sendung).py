import socket
import platform
import psutil
import ifaddr
import smtplib
from email.mime.text import MIMEText
import subprocess
import netifaces

def get_system_info():
    system_info = f"System: {platform.system()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    system_info += f"RAM: {psutil.virtual_memory().total} bytes\n"
    return system_info

def get_ip_addresses():
    ip_info = "IP Addresses:\n"
    for adapter in ifaddr.get_adapters():
        for ip in adapter.ips:
            ip_info += f"- {ip.ip}\n"

    return ip_info



def get_mac_address():
    mac_info = "MAC Address:\n"
    for interface in netifaces.interfaces():
        try:
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            mac_info += f"- {mac_address}\n"
        except KeyError:
            pass
    return mac_info

# Testen der Funktion
print(get_mac_address())

# Testen der Funktion
print(get_mac_address())

# Testen der Funktion
print(get_mac_address())

# Systeminformationen abrufen
system_info = get_system_info()

# IP-Adressen abrufen
ip_info = get_ip_addresses()

# MAC-Adresse abrufen
mac_info = get_mac_address()

# E-Mail Inhalt erstellen
email_content = f"{system_info}\n{ip_info}\n{mac_info}"

# E-Mail Konfiguration
sender_email = "YOUR EMAIL ADRESS HERE"
receiver_email = "YOUR EMAIL ADRESS HERE"
password = "YOUR EMAIL PASSWORD HERE"

message = MIMEText(email_content)
message["Subject"] = "System Information"
message["From"] = sender_email
message["To"] = receiver_email

# E-Mail senden
with smtplib.SMTP("THE SMPT SERVER OF YOUR EMAIL PROVIDER HERE", 587) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
