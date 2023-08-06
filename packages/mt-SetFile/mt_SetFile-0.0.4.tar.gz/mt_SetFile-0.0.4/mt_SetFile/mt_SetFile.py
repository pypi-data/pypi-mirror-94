#!/usr/bin/env python

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout,
    QSizePolicy, QLayout, QSpacerItem, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from datetime import datetime
import winreg, errno
import time
from glob2 import glob

import mt_UI

from . import myTextEdit

class MainUI(QtWidgets.QFrame):
    def __init__(self):
        super(MainUI, self).__init__() # Call init for inherited class
        
        self.setGeometry(300,300,900,80)
        self.setWindowTitle("Choose a configuration file...")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #   Container Widget
        widget = QtWidgets.QWidget(self)
        #   Layout of Container Widget
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(6, 6, 6, 6)
        self.mainLayout.setSpacing(8)
        widget.setLayout(self.mainLayout)
        
        self.hBoxLayout01 = QHBoxLayout()
        self.hBoxLayout02 = QHBoxLayout()
        #self.supHBoxLayout01 = QHBoxLayout()
        #self.hBoxLayout01.setSizeConstraint(QLayout.SetNoConstraint)
        #self.hBoxLayout02.setSizeConstraint(QLayout.SetNoConstraint)
        
        self.vBoxLayout01 = QVBoxLayout()
        
        self.spacerItem = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.searchComboBox = mt_UI.ExtendedCombo()
        self.searchComboBox.setMinimumContentsLength(25)
        self.searchComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        

        self.configLocation = 'C:\\Users\\max.luehmann\\Documents\\programming\\Git\\PortableGit\\source\\master\\Shared\\'
        print(self.configLocation)
        self.configFiles = glob(self.configLocation+'*.dat')
        self.configFilesShort = []
        for x in self.configFiles:
            self.configFilesShort.append(x.split('\\', -1)[-1])
        result = self.configFilesShort
        
        model = QtGui.QStandardItemModel()
        for i,word in enumerate(result):
            item = QtGui.QStandardItem(word)
            model.setItem(i, 0, item)
            
        
        #Create buttons
        self.swapButton = QPushButton(QIcon('../res/Refresh.png'),'',self)
        self.viewButton = QPushButton(QIcon('../res/view.png'),'',self)
        #Connect button signals
        self.swapButton.clicked.connect(self.swapFiles)
        self.viewButton.clicked.connect(self.openFile)
        
            
        self.currentFileLabel = QLabel('Current configuration file')
        ####################################################
        #          read config file from ini
        self.iniFile = 'C:\\ProgramData\\Fluke\\metcal.ini'
        self.string = 'config                ='
        with open(self.iniFile) as fp:
            for line in fp:
                if self.string in line:
                    print(line)
                    self.currentFile = line.split('=')[-1]
                else:
                    self.currentFile = 'F:\\METBASE\\Shared\\config.dat'
        self.currentFileDisplay = QLabel(self.currentFile)
        self.currentFileDisplay.setFixedSize(550,20)
        self.currentFileDisplay.setAlignment(Qt.AlignRight)
        #self.currentFileDisplay.setStyleSheet("background-color:#F8FF6B;")
        self.comboBoxLabel = QLabel("Select a configuration file")
            
        self.searchComboBox.setModel(model)
        self.searchComboBox.setModelColumn(0)
        
        self.hBoxLayout01.addWidget(self.comboBoxLabel)
        self.hBoxLayout01.addItem(self.spacerItem)
        self.hBoxLayout01.addWidget(self.searchComboBox)
        self.hBoxLayout01.addWidget(self.viewButton)
        
        self.hBoxLayout02.addWidget(self.currentFileLabel)
        self.hBoxLayout02.addItem(self.spacerItem)
        self.hBoxLayout02.addWidget(self.currentFileDisplay)
        self.hBoxLayout02.addWidget(self.swapButton)
        
        self.vBoxLayout01.addLayout(self.hBoxLayout02)
        self.vBoxLayout01.addLayout(self.hBoxLayout01)
        self.mainLayout.addLayout(self.vBoxLayout01)
        
    def swapFiles(self):
        old = self.currentFile
        new = self.configFiles[self.configFilesShort.index(self.searchComboBox.currentText())]
        print()
        print('current config file:')
        print(old)
        print('new config file:')
        print(new)
        print()
        self.currentFile = new
        with open(self.iniFile) as fp:
            for line in fp:
                if self.string in line:
                    tmpString = self.string+self.currentFile
                    line = tmpString
                else:
                    continue
                    
        self.currentFileDisplay.setText(self.currentFile)
        
        
    def openFile(self):
        file = self.configFiles[self.configFilesShort.index(self.searchComboBox.currentText())]
        self.viewer = myTextEdit.Main(file)
        self.viewer.show()

if __name__ == '__main__':
    import sys
    import os

    theCurrentDatetime = datetime.now()
    
    #ioMan = mt_FileMan.mtIOMan
    #logFile = ioMan.startLog(ioMan)

    QtCore.pyqtRemoveInputHook()
    app = QtWidgets.QApplication(sys.argv) # Create QApplication instance
    
    window = MainUI() # Create MainUI instance
    window.show()
    sys.exit(app.exec_()) # Start the app
