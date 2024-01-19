import sys
import fitz
import os
import re
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QDir

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


#Szczególy raty
pattern1 = re.compile(r"(Spłata raty\n)([0-9\s,].*)(PLN)([0-9\s,].*)(PLN)([0-9\s,].*)(PLN)")
#Nadpłaty
pattern2 = re.compile(r"(Spłata raty pozaplanowej\n)([0-9\s,].*)(PLN)")
#Harmonogram
pattern3 = re.compile(r"(Płatność\n)([0-9\s,].*)(\n?PLN)([0-9\s,].*)(\n?PLN)([0-9\s,].*)(\n?PLN)([0-9\s,].*)")
raty = []
kapital = []
odsetki = []
nadplaty = []
przyszla_rata = []
przyszly_kapital = []
przyszle_odsetki = []

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Calculate your loan")
window.setFixedWidth(1000)
window.move(1000, 200)
window.setStyleSheet("background: #161219;")

grid = QGridLayout()

class App(QWidget):
    def browse(self):
        dialog = QFileDialog()
        self.path = QDir.currentPath()
        dialog.setDirectory(self.path)
        dialog.setNameFilter("Documents (*.pdf)")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            self.filename = dialog.selectedFiles()
        # print(self.filename)
        # print(type(filename[-1]))
        # self.label.setText(self.filename[-1])
        self.open_file()

    def open_file(self):
        for i in self.filename:
            doc = fitz.open(i)
            text = ""
            for page in doc:
                text += page.get_text()
            for item in pattern1.finditer(text):
                raty.append(float(item.group(2).replace(u'\xa0', '').replace(',', '.')))
                kapital.append(float(item.group(4).replace(u'\xa0', '').replace(',', '.')))
                odsetki.append(float(item.group(6).replace(u'\xa0', '').replace(',', '.')))
            for item in pattern2.finditer(text):
                nadplaty.append(float(item.group(2).replace(u'\xa0', '').replace(',', '.')))

        suma_kapital = 0
        del kapital[10]  # zwielokrotnione
        for x in kapital:
            suma_kapital = suma_kapital + x

        suma_odsetki = 0
        del odsetki[10]  # zwielokrotnione
        for x in odsetki:
            suma_odsetki = suma_odsetki + x

        suma_nadplaty = 0
        for x in nadplaty:
            suma_nadplaty = suma_nadplaty + x

        self.message = (f'Historia:\nKapitał: {round(suma_kapital, 2)}'
                   f'\nNadpłaty: {suma_nadplaty}'
                   f'\nSuma: {suma_kapital + suma_nadplaty}'
                   f'\nPozostało: {round(160000 - (suma_kapital + suma_nadplaty), 2)}'
                   f'\nOdsetki: {round(suma_odsetki, 2)}')

        # print(message)
        self.frame2()
        # print(f'Historia:\nKapitał: {round(suma_kapital, 2)}')
        # print(f'Nadpłaty: {suma_nadplaty}')
        # print(f'Suma: {suma_kapital + suma_nadplaty}')
        # print(f'Pozostało: {round(160000 - (suma_kapital + suma_nadplaty), 2)}')
        # print(f'Odsetki: {round(suma_odsetki, 2)}')


    def main_button(self, text):
        button = QPushButton(text)
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{border: 4px solid '#BC006C';" +
            "border-radius: 15px;" +
            "font-size: 35px;" +
            "color: 'white';" +
            # "padding: 100x 100px;" +
            "margin: 100px 100px;}" +
            "*:hover{background: '#BC006C';}"
        )
        return button

    def frame1(self):
        image = QPixmap("logo.png")
        logo = QLabel()
        logo.setPixmap(image.scaled(200, 200, QtCore.Qt.KeepAspectRatio))
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet("margin-top: 100px;")
        logo.resize(20,20)
        widgets["logo"].append(logo)

        self.label = QLabel()
        self.label.setText("filename")
        self.label.setStyleSheet("color: 'white'")
        widgets["label"].append(self.label)

        #button

        button = self.main_button("Wybierz harmonogram")
        button.clicked.connect(self.browse)
        widgets["button"].append(button)

        button = self.main_button("Wybierz historie")
        button.clicked.connect(self.browse)
        widgets["button"].append(button)

        button = self.main_button("Oblicz")
        button.clicked.connect(self.browse)
        widgets["button"].append(button)

        grid.addWidget(widgets["logo"][-1], 0, 0)
        grid.addWidget(widgets["button"][-3], 1, 0)
        grid.addWidget(widgets["button"][-2], 2, 0)
        grid.addWidget(widgets["button"][-1], 3, 0)
        grid.addWidget(widgets["label"][-1], 4, 0)
        # grid.addWidget(self.label, 3, 0)
    def frame2(self):
        for widget in widgets:
            if widgets[widget] != []:
                widgets[widget][-1].hide()
            for i in range(0, len(widgets[widget])):
                widgets[widget].pop()
        self.label = QLabel()
        self.label.setText(self.message)
        self.label.setStyleSheet("color: 'white';" +
                                 "font-size: 35px")
        widgets["label"].append(self.label)
        grid.addWidget(widgets["label"][-1], 1, 0)

temp = App()
temp.frame1()
window.setLayout(grid)

window.show()
sys.exit(app.exec())