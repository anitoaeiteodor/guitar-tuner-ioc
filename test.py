from tokenize import String
import PySide6.QtCore
import sys
import random
import json
from PySide6 import QtCore, QtWidgets, QtGui
from playsound import playsound

class MainDisplay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QGridLayout(self)

        self.buttons = []
        letters = ['E', 'A', 'D', 'G', 'B', 'E']
        for i in range(6):
            self.buttons.append(QtWidgets.QPushButton(letters[i]))
        
        for button in self.buttons:
            self.layout.addWidget(button)
            button.clicked.connect(self.buttonClicked)
        
    def colorWidget(self, colorPallete):
        style = 'background-color: ' + colorPallete['main'] + '; ' + \
                'font-size: 32px'
        for i in range(len(self.buttons)):
            self.buttons[i].setStyleSheet(style)

    def buttonClicked(self):
        


class MenuButtons(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)

        self.buttonTuner = QtWidgets.QPushButton('Tuner')
        self.buttonTools = QtWidgets.QPushButton('Tools')

        self.buttonTuner.setStyleSheet('padding: 0px')

        self.layout.addWidget(self.buttonTuner)
        self.layout.addWidget(self.buttonTools)

    def colorWidget(self, colorPallete):
        self.buttonTools.setStyleSheet('background-color: ' + colorPallete['main'])
        self.buttonTuner.setStyleSheet('background-color: ' + colorPallete['main'])

    

class GuitarTuner(QtWidgets.QWidget):
    def __init__(self, colors):
        super().__init__()

        self.colorPallete = colors

        # self.background = QtWidgets.QLabel('', alignment=QtCore.Qt.AlignCenter)
        # self.background.setMargin(0)


        self.layout = QtWidgets.QVBoxLayout(self)
        # self.layout.addWidget(self.background)
        
        self.mainDisplay = MainDisplay()
        self.layout.addWidget(self.mainDisplay)

        self.menu = MenuButtons()
        self.layout.addWidget(self.menu)

        self.colorWidget()

    def colorWidget(self):
        self.setStyleSheet('background-color: ' + self.colorPallete['background'])
        self.menu.colorWidget(self.colorPallete)
        self.mainDisplay.colorWidget(self.colorPallete)


def loadTheme(path: String) -> String:
    fileContent = ''
    
    with open(path) as colors:
        fileContent = colors.read()
    
    return json.loads(fileContent)


if __name__ == "__main__":
    
    colors = loadTheme('./themes/darkTheme.json')
    app = QtWidgets.QApplication([])

    widget = GuitarTuner(colors)
    widget.resize(500, 600)
    widget.show()

    sys.exit(app.exec())