# -*- coding: utf-8 -*-


import random
from PyQt5 import QtCore, QtGui, QtWidgets

class PointerButton(QtWidgets.QPushButton):
    def __init__(self,num):
        super().__init__()
        self.number=num

    def getNumber(self):
        return self.number

class Ui_Form(QtWidgets.QMainWindow):

    arrow='⬆'
    #↑

    def __init__(self,col,pointer,st):
        super().__init__()
        self.initUI(col,pointer,st)

    def pointerBtnClick(self):
        sender=self.sender()
        self.tapeButtons[self.__pointer].setText('')
        self.__pointer=sender.getNumber()
        sender.setText(self.arrow)

    def setPointer(self,n):
        if (n>self.__columns-1) or n<0:
            return False, 'index out of range'
        else:
            self.tapeButtons[self.__pointer].setText('')
            self.tapeButtons[n].setText(self.arrow)
            self.__pointer=n
            return True, None

    def fillButtons(self):
        self.tapeButtons=[]
        for i in range(self.__columns):
            self.tapeButtons.append(PointerButton(i))
            self.tapeButtons[i].setFixedWidth(30)
            self.tapeButtons[i].clicked.connect(self.pointerBtnClick)
            if i==self.__pointer:
                self.tapeButtons[i].setText(self.arrow)
            else:
                self.tapeButtons[i].setText('')
            self.tapeTable.setCellWidget(1,i,self.tapeButtons[i])
        self.tapeTable.resizeColumnsToContents()

    def destroyButtons(self):
        for button in self.tapeButtons:
            button.destroy()
            button=None
        self.tapeButtons=None

    def setColumns(self,col):
        self.__pointer=0
        self.__columns=col
        self.destroyButtons()
        self.tapeTable.setColumnCount(self.__columns)
        self.tapeTable.setHorizontalHeaderLabels(map(lambda x: str(x),range(self.__columns)))
        self.fillButtons()

    def btnClick(self):
        sender=self.sender()
        print(sender.text())
        self.setColumns(random.randrange(3,7))

    def initUI(self,col,pointer,st):

        self.__pointer=pointer
        self.__columns=col
        self.__states=st

        # actions
        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # menubar
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        #self.fileMenu.setTitle("&Файл")
        self.fileMenu.addAction(exitAction)

        # centralwidget's content
        # labels

        # tape table
        self.button = QtWidgets.QPushButton("aaaa")
        self.button.clicked.connect(self.btnClick)

        self.tapeTable=QtWidgets.QTableWidget()
        self.tapeTable.setRowCount(2)
        self.tapeTable.setColumnCount(self.__columns)

        self.tapeTable.verticalHeader().setVisible(False)

        self.fillButtons()

        # machine table
        self.machineTable=QtWidgets.QTableWidget()
        self.machineTable.setRowCount(self.__states)
        self.machineTable.setColumnCount(self.__columns)
        self.machineTable.setHorizontalHeaderLabels(map(lambda x: str(x),range(self.__columns)))
        self.machineTable.setVerticalHeaderLabels(map(lambda x: str(x),range(self.__states)))

        # layouts
        self.tapeScrollVBox = QtWidgets.QVBoxLayout()
        self.tapeScrollVBox.addWidget(self.tapeTable)

        self.machineScrollVBox = QtWidgets.QVBoxLayout()
        self.machineScrollVBox.addWidget(self.machineTable)

        self.tapeScrollArea = QtWidgets.QScrollArea()
        self.tapeScrollArea.setLayout(self.tapeScrollVBox)

        self.machineScrollArea = QtWidgets.QScrollArea()
        self.machineScrollArea.setLayout(self.machineScrollVBox)

        self.mainVBox = QtWidgets.QVBoxLayout()
        self.mainVBox.addWidget(self.tapeScrollArea)
        self.mainVBox.addWidget(self.machineScrollArea)
        self.mainVBox.addStretch(1)
        self.mainVBox.addWidget(self.button)

        # centralwidet
        self.uiwidget = QtWidgets.QWidget()
        self.uiwidget.setLayout(self.mainVBox)
        
        self.setCentralWidget(self.uiwidget)
        self.setGeometry(0, 0, 500, 300)
        self.setWindowTitle('Buttons')
