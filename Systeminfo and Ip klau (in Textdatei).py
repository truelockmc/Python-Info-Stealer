import socket
import platform

def get_system_info():
    system_info = f"System: {platform.system()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    return system_info

def get_ip_addresses():
    hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(hostname)[-1]
    ip_info = "IP Addresses:\n"
    for ip in ip_addresses:
        ip_info += f"- {ip}\n"
    return ip_info

# Systeminformationen abrufen
system_info = get_system_info()

# IP-Adressen abrufen
ip_info = get_ip_addresses()

# Informationen in eine Textdatei speichern
with open("system_info.txt", "w") as file:
    file.write(system_info)
    file.write("\n")
    file.write(ip_info)