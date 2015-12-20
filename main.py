#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lgmrszd'
__version__ = '0.0.1b'

import sys
from PyQt5 import QtWidgets

from gui import Ui_Form

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = Ui_Form(100,0,1)
    Form.show()
    sys.exit(app.exec_())