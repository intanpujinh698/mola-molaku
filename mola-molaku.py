import sys
import random
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve
from PySide6.QtGui import QPixmap

class MolaAkuarium(QLabel):
    def __init__(self, image_buka, image_tutup):
        super().__init__()
        
        # 1. Setup Gambar
        self.pixmap_buka = QPixmap(image_buka).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.pixmap_tutup = QPixmap(image_tutup).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(self.pixmap_buka)
        
        # 2. Setup Window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(150, 150)
        
        # 3. Animasi Berenang
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(3000)
        self.anim.setEasingCurve(QEasingCurve.InOutSine)
        
        # 4. Timer Bergerak (Berenang lalu Istirahat)
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.swim)
        self.move_timer.start(5000) # Bergerak setiap 5 detik
        
        # 5. Timer Kedipan
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink)
        self.blink_timer.start(3000) # Kedip tiap 3 detik
        
        self.reset_blink_timer = QTimer(self)
        self.reset_blink_timer.setSingleShot(True)
        self.reset_blink_timer.timeout.connect(self.reset_blink)
        
        self.swim()

    def blink(self):
        self.setPixmap(self.pixmap_tutup)
        self.reset_blink_timer.start(200) # Mata tertutup 0.2 detik

    def reset_blink(self):
        self.setPixmap(self.pixmap_buka)

    def swim(self):
        screen = QApplication.primaryScreen().geometry()
        new_x = random.randint(0, screen.width() - 150)
        new_y = random.randint(0, screen.height() - 150)
        
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(QPoint(new_x, new_y))
        self.anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Masukkan nama file gambar Anda di sini
    mola = MolaAkuarium("mola-molaku.png", "mola-molakuberkedip.png") 
    mola.show()
    
    sys.exit(app.exec())