import random
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve

app = QApplication([])

window = QWidget()
window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
window.setAttribute(Qt.WA_TranslucentBackground)
window.setStyleSheet("background: transparent;")

CHAR_WIDTH = 170
CHAR_HEIGHT = 170
window.resize(CHAR_WIDTH, CHAR_HEIGHT)

images = ["images/bike.png", "images/horse.png"]
chosen_image = random.choice(images)

label = QLabel()
label.setStyleSheet("background: transparent;")
pixmap = QPixmap(chosen_image)
flipped_pixmap = pixmap.transformed(QTransform().scale(-1, 1))
label.setPixmap(flipped_pixmap)
label.setScaledContents(True)

layout = QVBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)
layout.addWidget(label)
window.setLayout(layout)

# --- Sliding animation setup ---
screen = app.primaryScreen().availableGeometry()
screen_left = screen.x()
screen_top = screen.y()
screen_right = screen.x() + screen.width()
screen_height = screen.height()

start_y = screen_top + (screen_height // 2)

# Fully visible starting point at the right edge (not cut off)
start_x = screen_right - CHAR_WIDTH - 5
# Slides further inward, toward center
end_x = screen_right - CHAR_WIDTH - 600

window.setGeometry(start_x, start_y, CHAR_WIDTH, CHAR_HEIGHT)
window.show()

animation = QPropertyAnimation(window, b"geometry")
animation.setDuration(4000)   # 4 seconds - slower, easier to see
animation.setEasingCurve(QEasingCurve.OutCubic)  # smooth deceleration
animation.setStartValue(QRect(start_x, start_y, CHAR_WIDTH, CHAR_HEIGHT))
animation.setEndValue(QRect(end_x, start_y, CHAR_WIDTH, CHAR_HEIGHT))
animation.start()

app.exec()