#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lgmrszd'
__version__ = '0.0.1b'

import sys
from PyQt5 import QtWidgets

import turmach
from gui import MyForm

TuringMachine=turmach.TuringMachine()

app = QtWidgets.QApplication(sys.argv)
Form = MyForm(100, 0, 1, TuringMachine.getAlphabet(), TuringMachine.getTape(), TuringMachine.getNull())
Form.show()

sys.exit(app.exec_())