import random
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap

app = QApplication([])

window = QWidget()
window.setWindowTitle("Mini Lipi Companion")
window.resize(400, 400)

# List of available character images
images = ["images/bike.png", "images/horse.png"]
chosen_image = random.choice(images)

label = QLabel()
pixmap = QPixmap(chosen_image)
label.setPixmap(pixmap)

layout = QVBoxLayout()
layout.addWidget(label)
window.setLayout(layout)

window.show()

app.exec()