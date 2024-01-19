import sys
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

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Calculate your loan")
window.setFixedWidth(1000)
# window.move(2700, 200)
window.setStyleSheet("background: #161219;")

grid = QGridLayout()

def clear():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

# def start():
#     clear()
#     browse()

def browse():
    dialog = QFileDialog()
    dialog.setDirectory(QDir.currentPath())
    dialog.setNameFilter("Documents (*.pdf)")
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    dialog.setViewMode(QFileDialog.ViewMode.List)
    if dialog.exec():
        filename = dialog.selectedFiles()
    print(filename[-1])
    # print(type(filename[-1]))
    label.setText(filename[-1])



def main_button(text):
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

def create_buttons(answer, l_margin, r_margin):
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        "margin-left: " + str(l_margin) + "px;" +
        "margin-right: " + str(r_margin) + "px;" +
        "border-radius: 25px;" +
        "font-size: 16px;" +
        "color: 'white';" +
        "font-family:'shanti';" +
        "padding: 15px 0;" +
        "margin-top: 20px}" +
        "*:hover{background: '#BC006C'}"
    )
    return button

def frame1():
    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)

    label = QLabel()
    label.setText("filename")
    label.setStyleSheet("color: 'white'")
    # widgets["label"].append(label)

    #button

    button = main_button("Wybierz historie")
    button.clicked.connect(browse)
    widgets["button"].append(button)

    button = main_button("Wybierz harmonogram")
    button.clicked.connect(browse)
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0)
    grid.addWidget(widgets["button"][-2], 1, 0)
    grid.addWidget(widgets["button"][-1], 2, 0)
    # grid.addWidget(widgets["label"][-1], 3, 0)
    grid.addWidget(label, 3, 0)

def frame2():
    score = QLabel("80")
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        '''
        font-size: 35px;
        color: 'white';
        padding: 25px 20px 0px 20px;
        margin: 20px 200px;
        background: '#64A314';
        border: 1px solid '#64A314';
        border-radius: 45px;
        '''
    )
    widgets["score"].append(score)

    # question widget
    question = QLabel("Placeholder text will go here blah blah")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"
    )
    widgets["question"].append(question)

    button1 = create_buttons("answer1", 85, 5)
    button2 = create_buttons("answer2", 5, 85)
    button3 = create_buttons("answer3", 85, 5)
    button4 = create_buttons("answer4", 5, 85)
    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)

frame1()

window.setLayout(grid)

window.show()
sys.exit(app.exec())

