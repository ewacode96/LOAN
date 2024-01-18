import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtGui import QCursor

widgets = {
    "logo": [],
    "label": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": []
}

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Calculate your loan")
window.setFixedWidth(1000)
# window.move(2700, 200)
window.setStyleSheet("background: #161219;")

grid = QGridLayout()

class App(QWidget):
    def browse(self):
        dialog = QFileDialog()
        dialog.setDirectory(r'C:\Users\ewasi\PycharmProjects\CFG\ING')
        dialog.setNameFilter("Documents (*.pdf)")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filename = dialog.selectedFiles()
        print(filename[-1])
        # print(type(filename[-1]))
        self.label.setText(filename[-1])

    def main_button(self, text):
        button = QPushButton(text)
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{border: 4px solid '#BC006C';" +
            "border-radius: 15px;" +
            "font-size: 35px;" +
            "color: 'white';" +
            "padding: 25x 0;" +
            "margin: 100px 200px;}" +
            "*:hover{background: '#BC006C';}"
        )
        return button

    def frame1(self):
        image = QPixmap("logo.png")
        logo = QLabel()
        logo.setPixmap(image)
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet("margin-top: 100px;")
        widgets["logo"].append(logo)

        self.label = QLabel()
        self.label.setText("filename")
        self.label.setStyleSheet("color: 'white'")
        widgets["label"].append(self.label)

        #button

        button = self.main_button("Wybierz historie")
        button.clicked.connect(self.browse)
        widgets["button"].append(button)

        button = self.main_button("Wybierz harmonogram")
        button.clicked.connect(self.browse)
        widgets["button"].append(button)

        grid.addWidget(widgets["logo"][-1], 0, 0)
        grid.addWidget(widgets["button"][-2], 1, 0)
        grid.addWidget(widgets["button"][-1], 2, 0)
        grid.addWidget(widgets["label"][-1], 3, 0)
        # grid.addWidget(self.label, 3, 0)

temp = App()
temp.frame1()
window.setLayout(grid)

window.show()
sys.exit(app.exec())