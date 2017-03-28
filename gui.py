# -*- coding: utf-8 -*-
__version__ = '0.0.1b'

import random
from PyQt5 import QtCore, QtGui, QtWidgets


class PointerButton(QtWidgets.QPushButton):
    def __init__(self, num):
        super().__init__()
        self.number = num

    def getNumber(self):
        return self.number


class MyForm(QtWidgets.QMainWindow):
    # ⬆↑
    arrow = '⬆'

    __lang = 'ru'
    __names = {
        'en': {
            'odt': 'Open file',
            'sdt': 'Save file',
            'fm': '&File',
            'of': '&Open…',
            'sf': '&Save…',
            'ea': '&Exit',
            'oft': 'Open File…',
            'sft': 'Save File…',
            'eat': 'Exit',
            'tam': "Tape and machine's rules",
            'alph': 'Alphabet:',
            'sdab': 'Set default alphabet',
            'sdnb': 'Set default null symbol'
        },
        'ru': {
            'odt': 'Открыть файл',
            'sdt': 'Сохранить файл',
            'fm': '&Файл',
            'of': '&Открыть…',
            'sf': '&Сохранить…',
            'ea': '&Выйти',
            'oft': 'Открыть файл…',
            'sft': 'Сохранить файл…',
            'eat': 'Выйти',
            'tam': 'Лента и правила машины',
            'alph': 'Алфавит:',
            'sdab': 'Установить алфавит по умолчанию',
            'sdnb': 'Установить нулевой символ по умолчанию'
        }
    }

    def translate(self, s):
        return self.__names[self.__lang][s]

    def __init__(self, col, pointer, st, alph, tape, null):
        super().__init__()
        self.initUI(col, pointer, st, alph, tape, null)

    def showOpenDialog(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, self.translate('odt'), '/home', 'XML files (*.xml)')[0]
        print(fname)

    def showSaveDialog(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, self.translate('sdt'), '/home', 'XML files (*.xml)')[0]
        print(fname)

    def pointerBtnClick(self):
        sender = self.sender()
        self.tapeButtons[self.__pointer].setText('')
        self.__pointer = sender.getNumber()
        sender.setText(self.arrow)

    def checkRule(self, rule):
        if len(rule) == 3 or 4 == len(rule):
            if rule[0] not in self.__alphabet:
                return False
            elif rule[2] not in 'lrsLRSлпнЛПН':
                return False
            else:
                try:
                    i = int(rule[1])
                except:
                    return False
                else:
                    if i > self.__states - 1:
                        return False
                    else:
                        return True
        else:
            return False

    def setPointer(self, n):
        if (n > self.__columns - 1) or n < 0:
            return False, 'index out of range'
        else:
            self.tapeButtons[self.__pointer].setText('')
            self.tapeButtons[n].setText(self.arrow)
            self.__pointer = n
            return True, None

    def fillButtons(self):
        self.tapeButtons = []
        for i in range(self.tapeTable.columnCount()):
            self.tapeButtons.append(PointerButton(i))
            self.tapeButtons[i].setFixedWidth(30)
            self.tapeButtons[i].clicked.connect(self.pointerBtnClick)
            if i == self.__pointer:
                self.tapeButtons[i].setText(self.arrow)
            else:
                self.tapeButtons[i].setText('')
            self.tapeTable.setCellWidget(1, i, self.tapeButtons[i])
        self.tapeTable.resizeColumnsToContents()

    def fillTapeTable(self):
        for i in range(self.__columns):
            self.tapeTable.setItem(0, i, QtWidgets.QTableWidgetItem(self.__tape[i]))

    def checkTape(self):
        valid=True
        invalids={}
        for i in range(self.__columns):
            t=self.tapeTable.item(0, i).text()
            if len(t)!=1:
                invalids[i]='t'
                print(i, ' total invalid')
                valid=False
                self.tapeButtons[i].setStyleSheet("*{background-color: red; border: 1px solid black; }")
            elif (t not in self.__alphabet) and (t!=self.__null):
                invalids[i]='i'
                print(i,' invalid')
                self.tapeButtons[i].setStyleSheet("*{background-color: yellow; border: 1px solid black; }")
                valid=False
            else:
                self.tapeButtons[i].setStyleSheet(QtWidgets.QPushButton().styleSheet())
        return valid

    def readTape(self):
        self.__tape = ''
        # print(self.__columns)
        for i in range(self.__columns):
            print(i)
            self.__tape += self.tapeTable.item(0, i).text()

    def destroyButtons(self):
        for button in self.tapeButtons:
            button.destroy()
            button = None
        self.tapeButtons = None

    def setColumns(self, col):
        self.readTape()
        self.__pointer = 0
        self.__columns = col
        self.destroyButtons()
        self.tapeTable.setColumnCount(self.__columns)
        self.tapeTable.setHorizontalHeaderLabels(map(lambda x: str(x), range(self.__columns)))
        self.fillButtons()
        self.__tape = (self.__tape + (col - len(self.__tape)) * self.__null)[:col]
        self.fillTapeTable()

    def checkBtnClick(self):
        print(self.checkTape())

    def initUI(self, col, pointer, st, alph, tape, null):

        self.__pointer = pointer
        self.__columns = col
        self.__states = st
        self.__alphabet = alph
        self.__tape = tape
        self.__null = null

        # actions
        openFile = QtWidgets.QAction(QtGui.QIcon('open.png'), self.translate('of'), self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip(self.translate('oft'))
        openFile.triggered.connect(self.showOpenDialog)

        saveFile = QtWidgets.QAction(QtGui.QIcon('save.png'), self.translate('sf'), self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip(self.translate('sft'))
        saveFile.triggered.connect(self.showSaveDialog)

        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), self.translate('ea'), self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(self.translate('eat'))
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # menubar
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu(self.translate('fm'))
        self.fileMenu.addAction(openFile)
        self.fileMenu.addAction(saveFile)
        self.fileMenu.addAction(exitAction)

        # centralwidget's content
        # labels

        # tape table
        self.tapeTable = QtWidgets.QTableWidget()
        self.tapeTable.setRowCount(2)
        self.tapeTable.setColumnCount(self.__columns)
        self.tapeTable.setHorizontalHeaderLabels(map(lambda x: str(x), range(self.__columns)))
        self.tapeTable.verticalHeader().setVisible(False)

        self.fillButtons()
        self.fillTapeTable()

        self.tapeTable.cellChanged.connect(self.checkTape)

        # machine table
        self.machineTable = QtWidgets.QTableWidget()
        self.machineTable.setRowCount(self.__states)
        self.machineTable.setColumnCount(len(self.__alphabet))
        self.machineTable.setHorizontalHeaderLabels(list(self.__alphabet))
        self.machineTable.setVerticalHeaderLabels(map(lambda x: str(x), range(self.__states)))

        # tape layouts
        self.tapeScrollVBox = QtWidgets.QVBoxLayout()
        self.tapeScrollVBox.addWidget(self.tapeTable)

        self.machineScrollVBox = QtWidgets.QVBoxLayout()
        self.machineScrollVBox.addWidget(self.machineTable)

        self.tapeScrollArea = QtWidgets.QScrollArea()
        self.tapeScrollArea.setLayout(self.tapeScrollVBox)

        self.machineScrollArea = QtWidgets.QScrollArea()
        self.machineScrollArea.setLayout(self.machineScrollVBox)

        self.tablesVBox = QtWidgets.QVBoxLayout()
        self.tablesVBox.addWidget(self.tapeScrollArea)
        self.tablesVBox.addWidget(self.machineScrollArea)

        self.tablesGroupBox = QtWidgets.QGroupBox(self.translate('tam'))
        self.tablesGroupBox.setLayout(self.tablesVBox)

        # alphabet widgets
        self.alphabetLabel = QtWidgets.QLabel(self.translate('alph'))

        self.alphabetLineEdit = QtWidgets.QLineEdit()
        self.alphabetLineEdit.setText(self.__alphabet)

        self.alphabetDefaultButton = QtWidgets.QPushButton(self.translate('sdab'))
        self.alphabetDefaultButton.clicked.connect(self.readTape)

        self.alphabetHBox = QtWidgets.QHBoxLayout()
        self.alphabetHBox.addWidget(self.alphabetLabel)
        self.alphabetHBox.addWidget(self.alphabetLineEdit)
        self.alphabetHBox.addWidget(self.alphabetDefaultButton)

        # null symbol widgets
        self.nullLabel = QtWidgets.QLabel('Null symbol:')

        self.nullLineEdit = QtWidgets.QLineEdit()
        self.nullLineEdit.setText(self.__null)
        self.nullLineEdit.setFixedWidth(20)

        self.nullDefaultButton = QtWidgets.QPushButton(self.translate('sdnb'))

        self.nullHBox = QtWidgets.QHBoxLayout()
        self.nullHBox.addWidget(self.nullLabel)
        self.nullHBox.addWidget(self.nullLineEdit)
        self.nullHBox.addWidget(self.nullDefaultButton)
        self.nullHBox.addStretch(1)

        self.alphabetAndNullVBox = QtWidgets.QVBoxLayout()
        self.alphabetAndNullVBox.addLayout(self.alphabetHBox)
        self.alphabetAndNullVBox.addLayout(self.nullHBox)

        self.checkButton = QtWidgets.QPushButton('Check tape')
        self.checkButton.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.checkButton.clicked.connect(self.checkBtnClick)

        self.alphabetAndNullAllHBox = QtWidgets.QHBoxLayout()
        self.alphabetAndNullAllHBox.addLayout(self.alphabetAndNullVBox)
        self.alphabetAndNullAllHBox.addWidget(self.checkButton)

        self.mainVBox = QtWidgets.QVBoxLayout()
        self.mainVBox.addWidget(self.tablesGroupBox)
        self.mainVBox.addLayout(self.alphabetAndNullAllHBox)
        self.mainVBox.addStretch(1)

        # centralwidet
        self.uiwidget = QtWidgets.QWidget()
        self.uiwidget.setLayout(self.mainVBox)

        self.setCentralWidget(self.uiwidget)
        self.setGeometry(0, 0, 500, 300)
        self.setWindowTitle('SimpleTuring, version %s' % __version__)
