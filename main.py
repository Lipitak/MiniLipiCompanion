import random
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer

app = QApplication([])

CHAR_WIDTH = 170
CHAR_HEIGHT = 230

images = ["images/bike.png", "images/horse.png"]

NORMAL_INTERVAL = 30000
SNOOZE_INTERVAL = 10000

no_dialogues = [
    "Jaldi piyo na please 🥺💧",
    "Tumhara body paani maang rahi hai!",
    "Ek glass paani, abhi ke abhi! 💧",
]

current_window = None
current_animation = None


def schedule_next(delay_ms):
    QTimer.singleShot(delay_ms, show_character)


def show_character():
    global current_window, current_animation
    print(">>> show_character() called")

    window = QWidget()
    window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    window.setAttribute(Qt.WA_TranslucentBackground)
    window.setStyleSheet("background: transparent;")
    window.resize(CHAR_WIDTH, CHAR_HEIGHT)

    chosen_image = random.choice(images)
    pixmap = QPixmap(chosen_image)
    flipped_pixmap = pixmap.transformed(QTransform().scale(-1, 1))

    image_label = QLabel()
    image_label.setStyleSheet("background: transparent;")
    image_label.setPixmap(flipped_pixmap)
    image_label.setScaledContents(True)
    image_label.setFixedSize(CHAR_WIDTH, 170)

    text_label = QLabel("Kya tumne paani pi liya? 💧")
    text_label.setWordWrap(True)
    text_label.setAlignment(Qt.AlignCenter)
    text_label.setStyleSheet("background-color: white; color: #333333; border: 2px solid #ffb6c1; "
        "border-radius: 10px; padding: 8px; font-size: 13px; font-weight: bold;" )
        

    yes_button = QPushButton("Yes ✅")
    no_button = QPushButton("No ❌")

    button_row = QHBoxLayout()
    button_row.addWidget(yes_button)
    button_row.addWidget(no_button)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(image_label)
    layout.addWidget(text_label)
    layout.addLayout(button_row)
    window.setLayout(layout)

    screen = app.primaryScreen().availableGeometry()
    screen_top = screen.y()
    screen_right = screen.x() + screen.width()
    screen_height = screen.height()

    start_y = screen_top + (screen_height // 2)
    start_x = screen_right - CHAR_WIDTH - 5
    end_x = screen_right - CHAR_WIDTH - 600

    window.setGeometry(start_x, start_y, CHAR_WIDTH, CHAR_HEIGHT)
    window.show()
    window.raise_()
    window.activateWindow()
    print(">>> window shown at", start_x, start_y, "size", CHAR_WIDTH, CHAR_HEIGHT)
    print(">>> is visible?", window.isVisible())

    animation = QPropertyAnimation(window, b"geometry")
    animation.setDuration(4000)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    animation.setStartValue(QRect(start_x, start_y, CHAR_WIDTH, CHAR_HEIGHT))
    animation.setEndValue(QRect(end_x, start_y, CHAR_WIDTH, CHAR_HEIGHT))
    animation.start()

    current_window = window
    current_animation = animation

    def handle_yes():
        window.close()
        schedule_next(NORMAL_INTERVAL)

    def handle_no():
        text_label.setText(random.choice(no_dialogues))
        yes_button.setEnabled(False)
        no_button.setEnabled(False)
        QTimer.singleShot(2500, window.close)
        schedule_next(SNOOZE_INTERVAL)

    yes_button.clicked.connect(handle_yes)
    no_button.clicked.connect(handle_no)


schedule_next(2000)

sys.exit(app.exec())