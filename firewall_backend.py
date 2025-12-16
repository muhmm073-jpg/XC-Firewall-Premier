import scapy.all as scapy
from scapy.all import conf
import threading
import queue
import time
import logging
import json
import os

# Sürücü hatasını önlemek için L3 moduna zorla
conf.L3socket = conf.L3socket

APP_NAME = "Xc Firewall"
APP_VERSION = "2.5"
RULES_FILE = "xc_rules.json" # Çakışma olmaması için özel isim

# İstatistikler
stats = {"total_packets": 0, "dropped_packets": 0, "blocked_ips": {}}

# Loglama Ayarı
logging.basicConfig(filename="firewall.log", level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s')

def load_xc_rules():
    """xc_rules.json dosyasından engelli IP listesini çeker"""
    if os.path.exists(RULES_FILE):
        try:
            with open(RULES_FILE, "r") as f:
                data = json.load(f)
                return data.get("blocked_ips", [])
        except Exception as e:
            print(f"Kural dosyasi okuma hatasi: {e}")
    return []

def apply_rules(packet, output_queue):
    global stats
    try:
        if packet.haslayer(scapy.IP):
            stats["total_packets"] += 1
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            
            # Güncel engelli listesini al
            blocked_ips = load_xc_rules()
            
            status = "ALLOW"
            reason = "Güvenli Trafik"
            
            # ENGELLEME KONTROLÜ
            if src_ip in blocked_ips or dst_ip in blocked_ips:
                status = "DROP"
                reason = "XC-BLOCK: Yasakli IP Tespit Edildi!"
                stats["dropped_packets"] += 1
                logging.warning(f"ENGELLEDİ: {src_ip} -> {dst_ip}")

            # GUI için paket verisi hazırla
            packet_data = {
                "time": time.strftime("%H:%M:%S"),
                "status": status,
                "source": src_ip,
                "destination": dst_ip,
                "port": packet.sport if hasattr(packet, "sport") else (packet.dport if hasattr(packet, "dport") else 0),
                "reason": reason
            }
            
            # Veriyi GUI kuyruğuna gönder
            output_queue.put(packet_data)

    except Exception as e:
        pass # Hatalı paketleri sessizce geç

def start_backend(interface_name):
    """Sniffer'ı ayrı bir kanalda başlatır"""
    output_queue = queue.Queue()
    
    def sniffer_thread():
        logging.info(f"Xc Sniffer aktif edildi: {interface_name}")
        # store=0 bellek şişmesini önler
        scapy.sniff(iface=interface_name, prn=lambda p: apply_rules(p, output_queue), store=0)

    thread = threading.Thread(target=sniffer_thread, daemon=True)
    thread.start()
    
    return output_queue, lambda: stats