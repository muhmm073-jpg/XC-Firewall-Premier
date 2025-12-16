import sys, queue, ctypes, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from scapy.all import conf

# Backend'den gerekli fonksiyonları çağırıyoruz
try:
    from firewall_backend import start_backend
except ImportError:
    print("HATA: firewall_backend.py dosyasi ayni klasorde bulunmali!")
    sys.exit(1)

# --- EKSIK OLAN FONKSIYON BURADA ---
def find_active_card():
    """Bilgisayardaki aktif internet kartini (Realtek vb.) bulur."""
    target_ip = "192.168.23.243" # Senin ozel IP adresin
    for n in conf.ifaces:
        if conf.ifaces[n].ip == target_ip:
            return n
    return conf.iface.name # Eger IP bulunamazsa varsayilani dondur

class BackendWorker(QThread):
    data_signal = pyqtSignal(dict)
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.q, self.get_stats_ref = start_backend(self.iface)
    def run(self):
        while True:
            try:
                data = self.q.get(timeout=1)
                self.data_signal.emit(data)
            except:
                continue

class XC_Firewall_Pro(QWidget):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.setWindowTitle("XC FIREWALL PREMIER v2.5")
        self.resize(1100, 700)
        self.setStyleSheet("background-color: #0b0f19; color: #cbd5e1;")
        
        # Dinamik Ikon Olusturucu
        self.set_dynamic_icon()
        
        self.init_ui()
        self.worker = BackendWorker(self.iface)
        self.worker.data_signal.connect(self.refresh_ui)
        self.worker.start()

    def set_dynamic_icon(self):
        pixmap = QPixmap(128, 128)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.moveTo(64, 10)
        path.cubicTo(110, 10, 110, 50, 110, 80)
        path.cubicTo(110, 110, 64, 120, 64, 120)
        path.cubicTo(64, 120, 18, 110, 18, 80)
        path.cubicTo(18, 50, 18, 10, 64, 10)
        
        painter.fillPath(path, QColor("#3b82f6"))
        font = QFont("Arial", 40, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("white"))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "XC")
        painter.end()
        
        self.my_icon = QIcon(pixmap)
        self.setWindowIcon(self.my_icon)
        QApplication.setWindowIcon(self.my_icon)

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QHBoxLayout()
        
        title_area = QVBoxLayout()
        title = QLabel("XC NETWORK SECURITY")
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #58a6ff;")
        self.status_lbl = QLabel(f"AKTIF: {self.iface}")
        self.status_lbl.setStyleSheet("color: #7ee787;")
        title_area.addWidget(title)
        title_area.addWidget(self.status_lbl)
        
        self.stats_lbl = QLabel("PAKET: 0 | ENGEL: 0")
        self.stats_lbl.setStyleSheet("font-size: 14pt; font-weight: bold; background: #161b22; padding: 10px; border-radius: 5px;")
        
        header.addLayout(title_area)
        header.addStretch()
        header.addWidget(self.stats_lbl)
        layout.addLayout(header)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["SAAT", "DURUM", "KAYNAK", "HEDEF", "PORT", "NOT"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("QTableWidget { background: #161b22; border: none; }")
        layout.addWidget(self.table)

    def refresh_ui(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        cols = [data["time"], data["status"], data["source"], data["destination"], str(data["port"]), data["reason"]]
        for i, val in enumerate(cols):
            item = QTableWidgetItem(val)
            if data["status"] == "DROP":
                item.setBackground(QColor("#7d1a1a"))
            self.table.setItem(row, i, item)
        
        s = self.worker.get_stats_ref()
        self.stats_lbl.setText(f"PAKET: {s['total_packets']} | ENGEL: {s['dropped_packets']}")
        
        if row > 15: self.table.scrollToBottom()
        if row > 500: self.table.setRowCount(0)

if __name__ == "__main__":
    # Windows Gorev Cubugu Ikonu Zorlamasi
    myappid = 'xc.firewall.premier.2.5' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Artik bu fonksiyonu tanimladigimiz icin hata vermeyecek
    active_iface = find_active_card()
    
    window = XC_Firewall_Pro(active_iface)
    window.show()
    sys.exit(app.exec())