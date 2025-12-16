# 🛡️ XC Firewall Premier v1.0
**Advanced Network Traffic Analysis & Security Management System**

XC Firewall Premier, Python ve Scapy tabanlı, düşük seviyeli (low-level) ağ paketlerini analiz eden ve gerçek zamanlı trafik kontrolü sağlayan profesyonel bir ağ güvenlik arayüzüdür.

## 🚀 Temel Özellikler
* **Deep Packet Inspection (DPI):** Ağ kartı üzerinden geçen tüm TCP, UDP ve ICMP paketlerini katman bazlı analiz eder.
* **Dynamic Rule Engine:** `xc_rules.json` üzerinden anlık olarak kural ekleme, silme ve düzenleme desteği.
* **IP & Port Filtering:** İstenmeyen IP adreslerini ve port trafiğini anında bloklama.
* **Real-time Logging:** Tüm ağ aktivitelerini görsel arayüzde anlık olarak raporlama.
* **Administrative Privilege:** Windows UAC entegrasyonu ile tam yetkili kernel erişimi.

## 🛠️ Teknik Altyapı
Bu proje, modern ağ güvenlik protokolleri ve asenkron programlama teknikleri kullanılarak geliştirilmiştir:
- **Language:** Python 3.12+
- **Network Engine:** Scapy (Packet Manipulation Toolkit)
- **GUI Framework:** PyQt6 (High-Performance Desktop UI)
- **Data Storage:** JSON Serialized Database

## 📋 Kurulum ve Çalıştırma

### Geliştirici Modu (Source Code)
Projeyi kaynak koddan çalıştırmak için gerekli kütüphaneleri yükleyin:
```bash
pip install scapy PyQt6
python firewall_gui.py
