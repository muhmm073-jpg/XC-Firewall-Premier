# 🛡️ XC-DEFENSE: Specialized Network Security Suite
**Industrial Grade Packet Filtering & Firewall Management Interface**

XC-DEFENSE, kritik ağ altyapıları için geliştirilmiş, düşük gecikmeli (low-latency) paket işleme ve dinamik kural yönetimi sunan özel bir güvenlik çözümüdür. Standart yazılımların aksine, Scapy motorunu özel bir GUI katmanı ile birleştirerek ağ yöneticilerine tam denetim sağlar.

## 🛡️ Yazılım Mimarisi ve Yetenekler
* **Kernel-Level Packet Sniffing:** Windows ağ sürücüleri ile entegre çalışarak paketleri çekirdek seviyesinde yakalar.
* **Custom Heuristic Analysis:** Trafik tipine (TCP/UDP/ICMP) göre özelleştirilmiş veri işleme döngüleri.
* **Static & Dynamic Blacklisting:** Kaynak ve hedef IP tabanlı, anlık güncellenebilir engelleyici mimari.
* **Privileged Execution Environment:** Güvenlik protokolleri gereği sadece yüksek yetkili kullanıcı modunda (Admin Mode) operasyonel faaliyet.

## 🛠️ Sistem Spesifikasyonları
| Bileşen | Teknoloji Stack |
| :--- | :--- |
| **Core Engine** | Python 3.12 (Asynchronous I/O) |
| **Packet Handler** | Scapy Specialized Library |
| **Interface** | PyQt6 Enterprise Framework |
| **Configuration** | JSON-based Rule Definition |

## 📦 Kurulum ve Operasyon

### Geliştirici Ortamı
Kaynak kodun stabilizasyonu için gerekli bağımlılıklar:
```bash
pip install scapy PyQt6
