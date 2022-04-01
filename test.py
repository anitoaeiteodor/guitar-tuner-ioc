from tokenize import String
import PySide6.QtCore
import sys
import random
import json
from PySide6 import QtCore, QtWidgets, QtGui
from playsound import playsound
import threading
import ttsAndstt
import time

command = ''

class MainDisplay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QGridLayout(self)

        self.buttons = []
        letters = ['E', 'A', 'D', 'G', 'B', 'E']
        self.soundPaths = ['./sounds/6th_String_E_64kb.mp3',
                      './sounds/5th_String_A_64kb.mp3',
                      './sounds/4th_String_D_64kb.mp3',
                      './sounds/3rd_String_G_64kb.mp3',
                      './sounds/2nd_String_B_64kb.mp3',
                      './sounds/1st_String_E_64kb.mp3',]
        
        methods = [self.buttonClicked6th,
                   self.buttonClicked5th,
                   self.buttonClicked4th,
                   self.buttonClicked3rd,
                   self.buttonClicked2nd,
                   self.buttonClicked1st]
        methods.reverse()
        for i in range(6):
            self.buttons.append(QtWidgets.QPushButton(letters[i]))
        
        for method, button in zip(methods, self.buttons):
            self.layout.addWidget(button)
            button.clicked.connect(method)

        threading.Thread(target=self.checkForCommands, daemon=True).start()
        
    def colorWidget(self, colorPallete):
        style = 'background-color: ' + colorPallete['main'] + '; ' + \
                'font-size: 32px'
        for i in range(len(self.buttons)):
            self.buttons[i].setStyleSheet(style)

    def checkForCommands(self):
        global command
        while True:
            if command != '':
                print(command)
            if command == 'A':
                self.buttonClicked2nd()
                command = ''
            if command == 'B':
                self.buttonClicked5th()
                command = ''
            if command == 'C':
                self.buttonClicked3rd()
                command = ''
            
            time.sleep(1)


    def buttonClicked6th(self):
        threading.Thread(target=playsound, args=(self.soundPaths[5],), daemon=True).start()

    def buttonClicked5th(self):
        threading.Thread(target=playsound, args=(self.soundPaths[4],), daemon=True).start()

    def buttonClicked4th(self):
        threading.Thread(target=playsound, args=(self.soundPaths[3],), daemon=True).start()

    def buttonClicked3rd(self):
        threading.Thread(target=playsound, args=(self.soundPaths[2],), daemon=True).start()

    def buttonClicked2nd(self):
        threading.Thread(target=playsound, args=(self.soundPaths[1],), daemon=True).start()

    def buttonClicked1st(self):
        threading.Thread(target=playsound, args=(self.soundPaths[0],), daemon=True).start()


class MenuButtons(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)

        self.buttonTuner = QtWidgets.QPushButton('Tuner')
        self.buttonTools = QtWidgets.QPushButton('Tools')
        self.buttonListen = QtWidgets.QPushButton('Listen')

        self.buttonTuner.setStyleSheet('padding: 0px')

        self.layout.addWidget(self.buttonTuner)
        self.layout.addWidget(self.buttonTools)
        self.layout.addWidget(self.buttonListen)

        self.buttonListen.clicked.connect(self.buttonClickedListen)
        self.beginListening = False

    def colorWidget(self, colorPallete):
        self.buttonTools.setStyleSheet('background-color: ' + colorPallete['main'])
        self.buttonTuner.setStyleSheet('background-color: ' + colorPallete['main'])
        self.buttonListen.setStyleSheet('background-color: ' + colorPallete['main'])

    def listenLoop(self):
        global command
        command = ttsAndstt.listen()
        print(command)

    def buttonClickedListen(self):
        self.beginListening = not self.beginListening
        threading.Thread(target=self.listenLoop, daemon=True).start()
        print(self.beginListening)


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
    
    colors = loadTheme('./themes/lightTheme.json')
    app = QtWidgets.QApplication([])

    widget = GuitarTuner(colors)
    widget.resize(500, 600)
    widget.show()

    sys.exit(app.exec())