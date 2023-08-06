# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI2.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np 
import matplotlib.pyplot as plt
import evpy as ev

class Ui_EVPY(object):
    def setupUi(self, EVPY):
        EVPY.setObjectName("EVPY")
        EVPY.resize(1259, 868)
        self.centralwidget = QtWidgets.QWidget(EVPY)
        self.centralwidget.setObjectName("centralwidget")
        self.sfBox = QtWidgets.QTabWidget(self.centralwidget)
        self.sfBox.setGeometry(QtCore.QRect(0, 0, 1281, 861))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sfBox.setFont(font)
        self.sfBox.setObjectName("sfBox")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 10, 651, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(50, 150, 401, 421))
        self.label_2.setObjectName("label_2")
        
        self.vBox = QtWidgets.QDoubleSpinBox(self.tab)
        self.vBox.setGeometry(QtCore.QRect(460, 250, 101, 25))
        self.vBox.setDecimals(5)
        self.vBox.setMinimum(-10000.0)
        self.vBox.setMaximum(10000.0)
        self.vBox.setObjectName("vBox")
        
        self.dBox = QtWidgets.QDoubleSpinBox(self.tab)
        self.dBox.setGeometry(QtCore.QRect(460, 320, 101, 25))
        self.dBox.setDecimals(5)
        self.dBox.setMinimum(-10000.0)
        self.dBox.setMaximum(10000.0)
        self.dBox.setObjectName("dBox")
        
        self.RmBox = QtWidgets.QDoubleSpinBox(self.tab)
        self.RmBox.setGeometry(QtCore.QRect(460, 400, 101, 25))
        self.RmBox.setDecimals(5)
        self.RmBox.setMinimum(-10000.0)
        self.RmBox.setMaximum(10000.0)
        self.RmBox.setObjectName("RmBox")
        
        self.ktBox = QtWidgets.QDoubleSpinBox(self.tab)
        self.ktBox.setGeometry(QtCore.QRect(460, 460, 101, 25))
        self.ktBox.setDecimals(5)
        self.ktBox.setMinimum(-10000.0)
        self.ktBox.setMaximum(10000.0)
        self.ktBox.setObjectName("ktBox")
        
        self.mperfButton = QtWidgets.QPushButton(self.tab)
        self.mperfButton.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.mperfButton.setObjectName("mperfButton")
        self.mperfButton.clicked.connect(self.motor_pred)
        
        self.label_22 = QtWidgets.QLabel(self.tab)
        self.label_22.setGeometry(QtCore.QRect(570, 250, 68, 19))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.tab)
        self.label_23.setGeometry(QtCore.QRect(570, 320, 161, 19))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.tab)
        self.label_24.setGeometry(QtCore.QRect(570, 400, 68, 19))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.tab)
        self.label_25.setGeometry(QtCore.QRect(570, 460, 191, 31))
        self.label_25.setObjectName("label_25")
        
        self.IOBox_2 = QtWidgets.QDoubleSpinBox(self.tab)
        self.IOBox_2.setGeometry(QtCore.QRect(460, 530, 101, 25))
        self.IOBox_2.setDecimals(5)
        self.IOBox_2.setMinimum(-10000.0)
        self.IOBox_2.setMaximum(10000.0)
        self.IOBox_2.setObjectName("IOBox_2")
        
        self.label_46 = QtWidgets.QLabel(self.tab)
        self.label_46.setGeometry(QtCore.QRect(570, 530, 68, 31))
        self.label_46.setObjectName("label_46")
        self.sfBox.addTab(self.tab, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.label_21 = QtWidgets.QLabel(self.tab_8)
        self.label_21.setGeometry(QtCore.QRect(50, 30, 701, 31))
        self.label_21.setObjectName("label_21")
        self.label_67 = QtWidgets.QLabel(self.tab_8)
        self.label_67.setGeometry(QtCore.QRect(100, 110, 221, 31))
        self.label_67.setObjectName("label_67")
        self.label_68 = QtWidgets.QLabel(self.tab_8)
        self.label_68.setGeometry(QtCore.QRect(100, 290, 311, 21))
        self.label_68.setObjectName("label_68")
        self.label_69 = QtWidgets.QLabel(self.tab_8)
        self.label_69.setGeometry(QtCore.QRect(100, 170, 321, 21))
        self.label_69.setObjectName("label_69")
        self.label_70 = QtWidgets.QLabel(self.tab_8)
        self.label_70.setGeometry(QtCore.QRect(100, 230, 291, 21))
        self.label_70.setObjectName("label_70")
        self.label_71 = QtWidgets.QLabel(self.tab_8)
        self.label_71.setGeometry(QtCore.QRect(100, 350, 281, 21))
        self.label_71.setObjectName("label_71")
        self.label_72 = QtWidgets.QLabel(self.tab_8)
        self.label_72.setGeometry(QtCore.QRect(100, 400, 281, 41))
        self.label_72.setObjectName("label_72")
        
        self.veff = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.veff.setGeometry(QtCore.QRect(490, 110, 101, 25))
        self.veff.setDecimals(5)
        self.veff.setMinimum(-10000.0)
        self.veff.setMaximum(10000.0)
        self.veff.setObjectName("veff")
        
        self.reff = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.reff.setGeometry(QtCore.QRect(490, 170, 101, 25))
        self.reff.setDecimals(5)
        self.reff.setMinimum(-10000.0)
        self.reff.setMaximum(10000.0)
        self.reff.setObjectName("reff")
        
        self.teff = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.teff.setGeometry(QtCore.QRect(490, 230, 101, 25))
        self.teff.setDecimals(5)
        self.teff.setMinimum(-10000.0)
        self.teff.setMaximum(10000.0)
        self.teff.setObjectName("teff")
        
        self.ieff = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.ieff.setGeometry(QtCore.QRect(490, 290, 101, 25))
        self.ieff.setDecimals(5)
        self.ieff.setMinimum(-10000.0)
        self.ieff.setMaximum(100000.0)
        self.ieff.setObjectName("ieff")
        
        self.toeff = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.toeff.setGeometry(QtCore.QRect(490, 350, 101, 25))
        self.toeff.setDecimals(5)
        self.toeff.setMinimum(-10000.0)
        self.toeff.setMaximum(10000.0)
        self.toeff.setObjectName("toeff")
        
        self.neff = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.neff.setGeometry(QtCore.QRect(490, 410, 101, 25))
        self.neff.setDecimals(5)
        self.neff.setMinimum(-10000.0)
        self.neff.setMaximum(10000.0)
        self.neff.setObjectName("neff")
        
        self.label_73 = QtWidgets.QLabel(self.tab_8)
        self.label_73.setGeometry(QtCore.QRect(610, 510, 111, 21))
        self.label_73.setObjectName("label_73")
        self.label_74 = QtWidgets.QLabel(self.tab_8)
        self.label_74.setGeometry(QtCore.QRect(610, 560, 131, 21))
        self.label_74.setObjectName("label_74")
        
        self.Noutput = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.Noutput.setGeometry(QtCore.QRect(760, 510, 101, 25))
        self.Noutput.setDecimals(5)
        self.Noutput.setMinimum(-10000.0)
        self.Noutput.setMaximum(10000.0)
        self.Noutput.setObjectName("Noutput")
        
        self.Ioutput = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.Ioutput.setGeometry(QtCore.QRect(760, 560, 101, 25))
        self.Ioutput.setDecimals(5)
        self.Ioutput.setMinimum(-10000.0)
        self.Ioutput.setMaximum(10000.0)
        self.Ioutput.setObjectName("Ioutput")
        
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_7.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.motor_efficiency)
        
        self.sfBox.addTab(self.tab_8, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 691, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(50, 150, 381, 411))
        self.label_4.setObjectName("label_4")
        
        self.NBox = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.NBox.setGeometry(QtCore.QRect(420, 180, 101, 25))
        self.NBox.setDecimals(5)
        self.NBox.setMinimum(-10000.0)
        self.NBox.setMaximum(10000.0)
        self.NBox.setObjectName("NBox")
        
        self.TBox_2 = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.TBox_2.setGeometry(QtCore.QRect(420, 250, 101, 25))
        self.TBox_2.setDecimals(5)
        self.TBox_2.setMinimum(-10000.0)
        self.TBox_2.setMaximum(10000.0)
        self.TBox_2.setObjectName("TBox_2")
        
        self.RmBox_2 = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.RmBox_2.setGeometry(QtCore.QRect(420, 390, 101, 25))
        self.RmBox_2.setDecimals(5)
        self.RmBox_2.setMinimum(-10000.0)
        self.RmBox_2.setMaximum(10000.0)
        self.RmBox_2.setObjectName("RmBox_2")
        
        self.IOBox = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.IOBox.setGeometry(QtCore.QRect(420, 470, 101, 25))
        self.IOBox.setDecimals(5)
        self.IOBox.setMinimum(-10000.0)
        self.IOBox.setMaximum(10000.0)
        self.IOBox.setObjectName("IOBox")
        
        self.numBox = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.numBox.setGeometry(QtCore.QRect(420, 540, 101, 25))
        self.numBox.setDecimals(5)
        self.numBox.setMinimum(-10000.0)
        self.numBox.setMaximum(10000.0)
        self.numBox.setObjectName("numBox")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.motor_contour)
        
        self.label_26 = QtWidgets.QLabel(self.tab_2)
        self.label_26.setGeometry(QtCore.QRect(530, 180, 91, 19))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.tab_2)
        self.label_27.setGeometry(QtCore.QRect(530, 250, 68, 19))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.tab_2)
        self.label_28.setGeometry(QtCore.QRect(530, 390, 68, 19))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(self.tab_2)
        self.label_29.setGeometry(QtCore.QRect(530, 460, 68, 41))
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.tab_2)
        self.label_30.setGeometry(QtCore.QRect(530, 540, 161, 19))
        self.label_30.setObjectName("label_30")
        
        self.KtBox = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.KtBox.setGeometry(QtCore.QRect(420, 320, 101, 25))
        self.KtBox.setDecimals(5)
        self.KtBox.setMinimum(-10000.0)
        self.KtBox.setMaximum(10000.0)
        self.KtBox.setObjectName("KtBox")
        
        self.label_47 = QtWidgets.QLabel(self.tab_2)
        self.label_47.setGeometry(QtCore.QRect(530, 320, 101, 31))
        self.label_47.setObjectName("label_47")
        self.sfBox.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 621, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(50, 100, 401, 311))
        self.label_6.setObjectName("label_6")
        
        self.T2Box = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.T2Box.setGeometry(QtCore.QRect(470, 170, 101, 25))
        self.T2Box.setDecimals(5)
        self.T2Box.setMinimum(-10000.0)
        self.T2Box.setMaximum(10000.0)
        self.T2Box.setObjectName("T2Box")
        
        self.XBox = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.XBox.setGeometry(QtCore.QRect(470, 240, 101, 25))
        self.XBox.setDecimals(5)
        self.XBox.setMinimum(-10000.0)
        self.XBox.setMaximum(10000.0)
        self.XBox.setObjectName("XBox")
        
        self.sBox = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.sBox.setGeometry(QtCore.QRect(470, 320, 101, 25))
        self.sBox.setDecimals(5)
        self.sBox.setMinimum(-10000.0)
        self.sBox.setMaximum(10000.0)
        self.sBox.setObjectName("sBox")
        
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.motor_size)
        
        self.label_31 = QtWidgets.QLabel(self.tab_3)
        self.label_31.setGeometry(QtCore.QRect(580, 170, 68, 19))
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.tab_3)
        self.label_32.setGeometry(QtCore.QRect(580, 240, 181, 19))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.tab_3)
        self.label_33.setGeometry(QtCore.QRect(580, 320, 151, 19))
        self.label_33.setObjectName("label_33")
        
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox.setGeometry(QtCore.QRect(700, 480, 101, 25))
        self.doubleSpinBox.setDecimals(5)
        self.doubleSpinBox.setMinimum(-10000.0)
        self.doubleSpinBox.setMaximum(10000.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(700, 530, 101, 25))
        self.doubleSpinBox_3.setDecimals(5)
        self.doubleSpinBox_3.setMinimum(-10000.0)
        self.doubleSpinBox_3.setMaximum(10000.0)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(700, 570, 101, 25))
        self.doubleSpinBox_4.setDecimals(5)
        self.doubleSpinBox_4.setMinimum(-10000.0)
        self.doubleSpinBox_4.setMaximum(10000.0)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        
        self.doubleSpinBox_5 = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_5.setGeometry(QtCore.QRect(700, 610, 101, 25))
        self.doubleSpinBox_5.setDecimals(5)
        self.doubleSpinBox_5.setMinimum(-10000.0)
        self.doubleSpinBox_5.setMaximum(10000.0)
        self.doubleSpinBox_5.setObjectName("doubleSpinBox_5")
        
        self.doubleSpinBox_6 = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_6.setGeometry(QtCore.QRect(700, 650, 101, 25))
        self.doubleSpinBox_6.setDecimals(5)
        self.doubleSpinBox_6.setMinimum(-10000.0)
        self.doubleSpinBox_6.setMaximum(10000.0)
        self.doubleSpinBox_6.setObjectName("doubleSpinBox_6")
        
        self.label_49 = QtWidgets.QLabel(self.tab_3)
        self.label_49.setGeometry(QtCore.QRect(540, 480, 101, 20))
        self.label_49.setObjectName("label_49")
        self.label_50 = QtWidgets.QLabel(self.tab_3)
        self.label_50.setGeometry(QtCore.QRect(540, 530, 121, 20))
        self.label_50.setObjectName("label_50")
        self.label_51 = QtWidgets.QLabel(self.tab_3)
        self.label_51.setGeometry(QtCore.QRect(540, 570, 141, 20))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.tab_3)
        self.label_52.setGeometry(QtCore.QRect(540, 610, 121, 20))
        self.label_52.setObjectName("label_52")
        self.label_53 = QtWidgets.QLabel(self.tab_3)
        self.label_53.setGeometry(QtCore.QRect(540, 650, 141, 20))
        self.label_53.setObjectName("label_53")
        self.label_60 = QtWidgets.QLabel(self.tab_3)
        self.label_60.setGeometry(QtCore.QRect(810, 480, 68, 31))
        self.label_60.setObjectName("label_60")
        self.label_61 = QtWidgets.QLabel(self.tab_3)
        self.label_61.setGeometry(QtCore.QRect(810, 530, 68, 19))
        self.label_61.setObjectName("label_61")
        self.label_62 = QtWidgets.QLabel(self.tab_3)
        self.label_62.setGeometry(QtCore.QRect(810, 570, 68, 19))
        self.label_62.setObjectName("label_62")
        self.label_63 = QtWidgets.QLabel(self.tab_3)
        self.label_63.setGeometry(QtCore.QRect(810, 610, 68, 19))
        self.label_63.setObjectName("label_63")
        self.label_64 = QtWidgets.QLabel(self.tab_3)
        self.label_64.setGeometry(QtCore.QRect(810, 650, 171, 31))
        self.label_64.setObjectName("label_64")
        self.sfBox.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.label_7 = QtWidgets.QLabel(self.tab_4)
        self.label_7.setGeometry(QtCore.QRect(20, 10, 551, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab_4)
        self.label_8.setGeometry(QtCore.QRect(40, 60, 631, 511))
        self.label_8.setObjectName("label_8")
        
        self.ImBox = QtWidgets.QDoubleSpinBox(self.tab_4)
        self.ImBox.setGeometry(QtCore.QRect(680, 90, 101, 25))
        self.ImBox.setDecimals(5)
        self.ImBox.setMinimum(-10000.0)
        self.ImBox.setMaximum(10000.0)
        self.ImBox.setObjectName("ImBox")
        
        self.PmBox = QtWidgets.QDoubleSpinBox(self.tab_4)
        self.PmBox.setGeometry(QtCore.QRect(680, 170, 101, 25))
        self.PmBox.setDecimals(5)
        self.PmBox.setMinimum(-10000.0)
        self.PmBox.setMaximum(10000.0)
        self.PmBox.setObjectName("PmBox")
        
        self.VBox = QtWidgets.QDoubleSpinBox(self.tab_4)
        self.VBox.setGeometry(QtCore.QRect(680, 240, 101, 25))
        self.VBox.setDecimals(5)
        self.VBox.setMinimum(-10000.0)
        self.VBox.setMaximum(10000.0)
        self.VBox.setObjectName("VBox")
        
        self.dBox_2 = QtWidgets.QDoubleSpinBox(self.tab_4)
        self.dBox_2.setGeometry(QtCore.QRect(680, 310, 101, 25))
        self.dBox_2.setDecimals(5)
        self.dBox_2.setMinimum(-10000.0)
        self.dBox_2.setMaximum(10000.0)
        self.dBox_2.setObjectName("dBox_2")
        
        self.fBox = QtWidgets.QDoubleSpinBox(self.tab_4)
        self.fBox.setGeometry(QtCore.QRect(680, 390, 101, 25))
        self.fBox.setDecimals(5)
        self.fBox.setMinimum(-10000.0)
        self.fBox.setMaximum(10000.0)
        self.fBox.setObjectName("fBox")
        
        self.RonBox = QtWidgets.QDoubleSpinBox(self.tab_4)
        self.RonBox.setGeometry(QtCore.QRect(680, 460, 101, 25))
        self.RonBox.setDecimals(5)
        self.RonBox.setMinimum(-10000.0)
        self.RonBox.setMaximum(10000.0)
        self.RonBox.setObjectName("RonBox")
        
        self.TonBox = QtWidgets.QDoubleSpinBox(self.tab_4)
        self.TonBox.setGeometry(QtCore.QRect(680, 530, 101, 25))
        self.TonBox.setDecimals(5)
        self.TonBox.setMinimum(-10000.0)
        self.TonBox.setMaximum(10000.0)
        self.TonBox.setObjectName("TonBox")
        
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_3.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.esc_pred)
        
        self.label_34 = QtWidgets.QLabel(self.tab_4)
        self.label_34.setGeometry(QtCore.QRect(790, 90, 68, 19))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.tab_4)
        self.label_35.setGeometry(QtCore.QRect(790, 170, 68, 19))
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.tab_4)
        self.label_36.setGeometry(QtCore.QRect(790, 240, 68, 19))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.tab_4)
        self.label_37.setGeometry(QtCore.QRect(790, 310, 161, 19))
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.tab_4)
        self.label_38.setGeometry(QtCore.QRect(790, 390, 68, 19))
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.tab_4)
        self.label_39.setGeometry(QtCore.QRect(790, 460, 68, 19))
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.tab_4)
        self.label_40.setGeometry(QtCore.QRect(790, 530, 81, 19))
        self.label_40.setObjectName("label_40")
        self.sfBox.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.label_9 = QtWidgets.QLabel(self.tab_5)
        self.label_9.setGeometry(QtCore.QRect(20, 10, 601, 91))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.tab_5)
        self.label_10.setGeometry(QtCore.QRect(50, 120, 531, 181))
        self.label_10.setObjectName("label_10")
        
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.tab_5)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(600, 170, 101, 25))
        self.doubleSpinBox_2.setDecimals(5)
        self.doubleSpinBox_2.setMinimum(-10000.0)
        self.doubleSpinBox_2.setMaximum(10000.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        
        self.doubleSpinBox_7 = QtWidgets.QDoubleSpinBox(self.tab_5)
        self.doubleSpinBox_7.setGeometry(QtCore.QRect(600, 250, 101, 25))
        self.doubleSpinBox_7.setDecimals(5)
        self.doubleSpinBox_7.setMinimum(-10000.0)
        self.doubleSpinBox_7.setMaximum(10000.0)
        self.doubleSpinBox_7.setObjectName("doubleSpinBox_7")
        
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_4.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.esc_size)
        
        self.label_41 = QtWidgets.QLabel(self.tab_5)
        self.label_41.setGeometry(QtCore.QRect(710, 170, 68, 19))
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.tab_5)
        self.label_42.setGeometry(QtCore.QRect(710, 250, 161, 19))
        self.label_42.setObjectName("label_42")
        
        self.doubleSpinBox_8 = QtWidgets.QDoubleSpinBox(self.tab_5)
        self.doubleSpinBox_8.setGeometry(QtCore.QRect(780, 490, 101, 25))
        self.doubleSpinBox_8.setDecimals(5)
        self.doubleSpinBox_8.setMinimum(-10000.0)
        self.doubleSpinBox_8.setMaximum(10000.0)
        self.doubleSpinBox_8.setObjectName("doubleSpinBox_8")
        
        self.doubleSpinBox_9 = QtWidgets.QDoubleSpinBox(self.tab_5)
        self.doubleSpinBox_9.setGeometry(QtCore.QRect(780, 540, 101, 25))
        self.doubleSpinBox_9.setDecimals(5)
        self.doubleSpinBox_9.setMinimum(-10000.0)
        self.doubleSpinBox_9.setMaximum(10000.0)
        self.doubleSpinBox_9.setObjectName("doubleSpinBox_9")
        
        self.label_54 = QtWidgets.QLabel(self.tab_5)
        self.label_54.setGeometry(QtCore.QRect(617, 490, 151, 20))
        self.label_54.setObjectName("label_54")
        self.label_55 = QtWidgets.QLabel(self.tab_5)
        self.label_55.setGeometry(QtCore.QRect(597, 540, 171, 20))
        self.label_55.setObjectName("label_55")
        self.label_65 = QtWidgets.QLabel(self.tab_5)
        self.label_65.setGeometry(QtCore.QRect(880, 490, 68, 31))
        self.label_65.setObjectName("label_65")
        self.label_66 = QtWidgets.QLabel(self.tab_5)
        self.label_66.setGeometry(QtCore.QRect(880, 540, 68, 19))
        self.label_66.setObjectName("label_66")
        self.sfBox.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.label_11 = QtWidgets.QLabel(self.tab_6)
        self.label_11.setGeometry(QtCore.QRect(20, 10, 731, 91))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_6)
        self.label_12.setGeometry(QtCore.QRect(40, 110, 391, 551))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.IBox = QtWidgets.QDoubleSpinBox(self.tab_6)
        self.IBox.setGeometry(QtCore.QRect(447, 150, 101, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.IBox.setFont(font)
        self.IBox.setDecimals(5)
        self.IBox.setMinimum(-10000.0)
        self.IBox.setMaximum(10000.0)
        self.IBox.setObjectName("IBox")
        
        self.tBox = QtWidgets.QDoubleSpinBox(self.tab_6)
        self.tBox.setGeometry(QtCore.QRect(447, 220, 101, 25))
        self.tBox.setDecimals(5)
        self.tBox.setMinimum(-10000.0)
        self.tBox.setMaximum(10000.0)
        self.tBox.setObjectName("tBox")
        
        self.QBox = QtWidgets.QDoubleSpinBox(self.tab_6)
        self.QBox.setGeometry(QtCore.QRect(447, 320, 101, 25))
        self.QBox.setDecimals(5)
        self.QBox.setMinimum(-10000.0)
        self.QBox.setMaximum(10000.0)
        self.QBox.setObjectName("QBox")
        
        self.n_serBox = QtWidgets.QDoubleSpinBox(self.tab_6)
        self.n_serBox.setGeometry(QtCore.QRect(447, 490, 101, 25))
        self.n_serBox.setDecimals(5)
        self.n_serBox.setMinimum(-10000.0)
        self.n_serBox.setMaximum(10000.0)
        self.n_serBox.setObjectName("n_serBox")
        
        self.n_prllBox = QtWidgets.QDoubleSpinBox(self.tab_6)
        self.n_prllBox.setGeometry(QtCore.QRect(447, 560, 101, 25))
        self.n_prllBox.setDecimals(5)
        self.n_prllBox.setMinimum(-10000.0)
        self.n_prllBox.setMaximum(10000.0)
        self.n_prllBox.setObjectName("n_prllBox")
        
        self.pkrtBox = QtWidgets.QDoubleSpinBox(self.tab_6)
        self.pkrtBox.setGeometry(QtCore.QRect(447, 630, 101, 25))
        self.pkrtBox.setDecimals(5)
        self.pkrtBox.setMinimum(-10000.0)
        self.pkrtBox.setMaximum(10000.0)
        self.pkrtBox.setObjectName("pkrtBox")
        
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_5.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.batt_pred)
        
        self.label_15 = QtWidgets.QLabel(self.tab_6)
        self.label_15.setGeometry(QtCore.QRect(560, 150, 68, 19))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.tab_6)
        self.label_16.setGeometry(QtCore.QRect(560, 220, 68, 19))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.tab_6)
        self.label_17.setGeometry(QtCore.QRect(560, 320, 81, 19))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.tab_6)
        self.label_18.setGeometry(QtCore.QRect(560, 490, 161, 19))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.tab_6)
        self.label_19.setGeometry(QtCore.QRect(560, 560, 161, 19))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.tab_6)
        self.label_20.setGeometry(QtCore.QRect(560, 630, 151, 19))
        self.label_20.setObjectName("label_20")
        
        self.RBox = QtWidgets.QDoubleSpinBox(self.tab_6)
        self.RBox.setGeometry(QtCore.QRect(447, 410, 101, 25))
        self.RBox.setDecimals(5)
        self.RBox.setMinimum(-10000.0)
        self.RBox.setMaximum(10000.0)
        self.RBox.setObjectName("RBox")
        
        self.label_48 = QtWidgets.QLabel(self.tab_6)
        self.label_48.setGeometry(QtCore.QRect(560, 410, 68, 19))
        self.label_48.setObjectName("label_48")
        self.sfBox.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.label_13 = QtWidgets.QLabel(self.tab_7)
        self.label_13.setGeometry(QtCore.QRect(20, 10, 631, 41))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.tab_7)
        self.label_14.setGeometry(QtCore.QRect(50, 90, 541, 291))
        self.label_14.setObjectName("label_14")
        
        self.tBox_2 = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.tBox_2.setGeometry(QtCore.QRect(650, 170, 101, 25))
        self.tBox_2.setDecimals(5)
        self.tBox_2.setMinimum(-10000.0)
        self.tBox_2.setMaximum(10000.0)
        self.tBox_2.setObjectName("tBox_2")
        
        self.eBox = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.eBox.setGeometry(QtCore.QRect(650, 240, 101, 25))
        self.eBox.setDecimals(5)
        self.eBox.setMinimum(-10000.0)
        self.eBox.setMaximum(10000.0)
        self.eBox.setObjectName("eBox")
        
        self.rhoBox = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.rhoBox.setGeometry(QtCore.QRect(650, 310, 101, 25))
        self.rhoBox.setDecimals(5)
        self.rhoBox.setMinimum(-10000.0)
        self.rhoBox.setMaximum(10000.0)
        self.rhoBox.setObjectName("rhoBox")
        
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_7)
        self.pushButton_6.setGeometry(QtCore.QRect(940, 510, 112, 34))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.batt_size)
        
        self.label_43 = QtWidgets.QLabel(self.tab_7)
        self.label_43.setGeometry(QtCore.QRect(770, 170, 68, 19))
        self.label_43.setObjectName("label_43")
        self.label_44 = QtWidgets.QLabel(self.tab_7)
        self.label_44.setGeometry(QtCore.QRect(770, 240, 68, 31))
        self.label_44.setObjectName("label_44")
        self.label_45 = QtWidgets.QLabel(self.tab_7)
        self.label_45.setGeometry(QtCore.QRect(770, 310, 91, 31))
        self.label_45.setObjectName("label_45")
        
        self.doubleSpinBox_10 = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.doubleSpinBox_10.setGeometry(QtCore.QRect(750, 490, 101, 25))
        self.doubleSpinBox_10.setDecimals(5)
        self.doubleSpinBox_10.setMinimum(-10000.0)
        self.doubleSpinBox_10.setMaximum(10000.0)
        self.doubleSpinBox_10.setObjectName("doubleSpinBox_10")
        
        self.doubleSpinBox_11 = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.doubleSpinBox_11.setGeometry(QtCore.QRect(750, 540, 101, 25))
        self.doubleSpinBox_11.setDecimals(5)
        self.doubleSpinBox_11.setMinimum(-10000.0)
        self.doubleSpinBox_11.setMaximum(10000.0)
        self.doubleSpinBox_11.setObjectName("doubleSpinBox_11")
        
        self.label_56 = QtWidgets.QLabel(self.tab_7)
        self.label_56.setGeometry(QtCore.QRect(470, 490, 281, 31))
        self.label_56.setObjectName("label_56")
        self.label_57 = QtWidgets.QLabel(self.tab_7)
        self.label_57.setGeometry(QtCore.QRect(450, 530, 301, 31))
        self.label_57.setObjectName("label_57")
        self.label_58 = QtWidgets.QLabel(self.tab_7)
        self.label_58.setGeometry(QtCore.QRect(860, 480, 68, 31))
        self.label_58.setObjectName("label_58")
        self.label_59 = QtWidgets.QLabel(self.tab_7)
        self.label_59.setGeometry(QtCore.QRect(860, 540, 68, 19))
        self.label_59.setObjectName("label_59")
        self.sfBox.addTab(self.tab_7, "")
        
        EVPY.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(EVPY)
        self.statusbar.setObjectName("statusbar")
        EVPY.setStatusBar(self.statusbar)
        self.actionPerformance = QtWidgets.QAction(EVPY)
        self.actionPerformance.setObjectName("actionPerformance")
        self.actionContour = QtWidgets.QAction(EVPY)
        self.actionContour.setObjectName("actionContour")
        self.actionSize = QtWidgets.QAction(EVPY)
        self.actionSize.setObjectName("actionSize")
        self.actionPrediction = QtWidgets.QAction(EVPY)
        self.actionPrediction.setObjectName("actionPrediction")
        self.actionSize_2 = QtWidgets.QAction(EVPY)
        self.actionSize_2.setObjectName("actionSize_2")
        self.actionLosses = QtWidgets.QAction(EVPY)
        self.actionLosses.setObjectName("actionLosses")
        self.actionSize_3 = QtWidgets.QAction(EVPY)
        self.actionSize_3.setObjectName("actionSize_3")

        self.retranslateUi(EVPY)
        self.sfBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(EVPY)

    def retranslateUi(self, EVPY):
        _translate = QtCore.QCoreApplication.translate
        EVPY.setWindowTitle(_translate("EVPY", "EVPY"))
        self.label.setText(_translate("EVPY", "Predict torque, power, current, and efficiency over a range of speeds.\n"
"Uses 3 high-level component parameters (Rm, kt, I0) and throttle.\n"
"Applicable to sensorless, six-step commutation brushless DC motors."))
        self.label_2.setText(_translate("EVPY", "\n"
"\n"
"\n"
"Voltage of the DC bus\n"
"\n"
"\n"
"Non-Dimentional throttle setting (duty ratio)\n"
"\n"
"\n"
"Motor resistance (phase to phase)\n"
"\n"
"\n"
"Torque constant of motor\n"
"\n"
"\n"
"No-load current of motor"))
        self.mperfButton.setText(_translate("EVPY", "Run"))
        self.label_22.setText(_translate("EVPY", "Volts"))
        self.label_23.setText(_translate("EVPY", "Non-Dimensional"))
        self.label_24.setText(_translate("EVPY", "Ohms"))
        self.label_25.setText(_translate("EVPY", "Newton-Meter/Amp"))
        self.label_46.setText(_translate("EVPY", "Amps"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab), _translate("EVPY", "Motor Performance"))
        self.label_21.setText(_translate("EVPY", "Predicts the eficcency and current draw at a specified torque and speed"))
        self.label_67.setText(_translate("EVPY", "Voltage of the DC bus"))
        self.label_68.setText(_translate("EVPY", "No load current of the motor"))
        self.label_69.setText(_translate("EVPY", "Motor Resistance (Phase to Phase)"))
        self.label_70.setText(_translate("EVPY", "Torque conasant of the motor"))
        self.label_71.setText(_translate("EVPY", "Desired Torque"))
        self.label_72.setText(_translate("EVPY", "Desired Speed"))
        self.label_73.setText(_translate("EVPY", "Efficiency"))
        self.label_74.setText(_translate("EVPY", "Current draw"))
        self.pushButton_7.setText(_translate("EVPY", "Run"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab_8), _translate("EVPY", "Motor Efficiency"))
        self.label_3.setText(_translate("EVPY", "Predicts motor efficiency within the motor\'s rated operating window.\n"
"Uses 3 high-level component parameters (Rm, kt, I0).\n"
"Applicable to sensorless, six-step commutation brushless DC motors.\n"
"DOES NOT factor in harmonics!"))
        self.label_4.setText(_translate("EVPY", "\n"
"Rated motor speed\n"
"\n"
"\n"
"Rated motor torque\n"
"\n"
"\n"
"Torque constant of motor\n"
"\n"
"\n"
"Motor resistance (phase to phase)\n"
"\n"
"\n"
"No-load current of motor\n"
"\n"
"\n"
"Number of data points along each axis"))
        self.pushButton_2.setText(_translate("EVPY", "Run"))
        self.label_26.setText(_translate("EVPY", "rev/min"))
        self.label_27.setText(_translate("EVPY", "N*m"))
        self.label_28.setText(_translate("EVPY", "Ohms"))
        self.label_29.setText(_translate("EVPY", "Amps"))
        self.label_30.setText(_translate("EVPY", "Non-Dimensional"))
        self.label_47.setText(_translate("EVPY", "N*m/Amp"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab_2), _translate("EVPY", "Motor Contour"))
        self.label_5.setText(_translate("EVPY", "Predict mass, diameter, length, figure of merit for given torque, D/L.\n"
"Default shear stress is for sub-500 gram BLDC motors."))
        self.label_6.setText(_translate("EVPY", "\n"
"Continuous torque required of motor\n"
"\n"
"\n"
"Stator aspect ratio (D/L)\n"
"\n"
"(OPTIONAL)\n"
"Shear stress used to size the initial volume\n"
"default of 5.5 kPa is a conservative est."))
        self.pushButton.setText(_translate("EVPY", "Run"))
        self.label_31.setText(_translate("EVPY", "N*m"))
        self.label_32.setText(_translate("EVPY", "Non-Dimensional"))
        self.label_33.setText(_translate("EVPY", "Pa (N/m^2)"))
        self.label_49.setText(_translate("EVPY", "Total Mass"))
        self.label_50.setText(_translate("EVPY", "Total volume"))
        self.label_51.setText(_translate("EVPY", "Outer Diameter"))
        self.label_52.setText(_translate("EVPY", "Outer Length"))
        self.label_53.setText(_translate("EVPY", "Motor Constant"))
        self.label_60.setText(_translate("EVPY", "kg"))
        self.label_61.setText(_translate("EVPY", "m^3"))
        self.label_62.setText(_translate("EVPY", "m"))
        self.label_63.setText(_translate("EVPY", "m"))
        self.label_64.setText(_translate("EVPY", "N*m/ sqrt(Ohms)"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab_3), _translate("EVPY", "Motor Size"))
        self.label_7.setText(_translate("EVPY", "Predict ESC losses given specs and motor performance."))
        self.label_8.setText(_translate("EVPY", "\n"
"Current pulled by the motor\n"
"\n"
"\n"
"Power pulled by the motor\n"
"\n"
"\n"
"The input (DC) voltage to the ESC\n"
"\n"
"\n"
"The nondimensional throttle setting (duty ratio)\n"
"\n"
"\n"
"The switching frequency of the ESC, about 8-32 kHz\n"
"\n"
"\n"
"The R_ds_ON measure of the MOSFETs in the ESC, about 5-20mOhms\n"
"\n"
"\n"
"The transition period of the MOSFETs, about 1 microsecond"))
        self.pushButton_3.setText(_translate("EVPY", "Run"))
        self.label_34.setText(_translate("EVPY", "Amps"))
        self.label_35.setText(_translate("EVPY", "Watts"))
        self.label_36.setText(_translate("EVPY", "Volts"))
        self.label_37.setText(_translate("EVPY", "Non-Dimensional"))
        self.label_38.setText(_translate("EVPY", "Hertz"))
        self.label_39.setText(_translate("EVPY", "Ohms"))
        self.label_40.setText(_translate("EVPY", "seconds"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab_4), _translate("EVPY", "ESC Losses"))
        self.label_9.setText(_translate("EVPY", "Predict the ESC volume and mass using a purely empirical fit.\n"
"Empirical data collected from 3 KDE, Castle, and HobbyWing data.\n"
"Nearly uniform trends among all three datasets."))
        self.label_10.setText(_translate("EVPY", "\n"
"The required continuous power output of the ESC\n"
"\n"
"(OPTIONAL)\n"
"a safety factor for the prediction hobby rule of thumb is 2.0"))
        self.pushButton_4.setText(_translate("EVPY", "Run"))
        self.label_41.setText(_translate("EVPY", "Watts"))
        self.label_42.setText(_translate("EVPY", "Non-Dimensional"))
        self.label_54.setText(_translate("EVPY", "Mass of the ESC"))
        self.label_55.setText(_translate("EVPY", "Volume of the ESC"))
        self.label_65.setText(_translate("EVPY", "kg"))
        self.label_66.setText(_translate("EVPY", "m^3"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab_5), _translate("EVPY", "ESC Size"))
        self.label_11.setText(_translate("EVPY", "Predict the entire pack\'s instantaneous terminal voltage under load.\n"
"Uses empirical state-of-charge curve fit obtained from Chen and Mora.\n"
"https://doi.org/10.1109/TEC.2006.874229"))
        self.label_12.setText(_translate("EVPY", "\n"
"The current draw at the battery terminals\n"
"\n"
"\n"
"The instant in time\n"
"\n"
"\n"
"The rated capacity of the battery unit\n"
"in the tens of mili-Ohms range\n"
"\n"
"\n"
"The internal resistance of the battery unit\n"
"in the tens of mili-Ohms range\n"
"\n"
"(OPTIONAL)\n"
"The number of battery units in series\n"
"\n"
"(OPTIONAL)\n"
"The number of battery units in parallel\n"
"\n"
"(OPTIONAL)\n"
"The peukert constant of the battery"))
        self.pushButton_5.setText(_translate("EVPY", "Run"))
        self.label_15.setText(_translate("EVPY", "Amps"))
        self.label_16.setText(_translate("EVPY", "Hours"))
        self.label_17.setText(_translate("EVPY", "Amp*hr"))
        self.label_18.setText(_translate("EVPY", "Non-Dimensional"))
        self.label_19.setText(_translate("EVPY", "Non-Dimensional"))
        self.label_20.setText(_translate("EVPY", "Non-Dimensinal"))
        self.label_48.setText(_translate("EVPY", "Ohms"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab_6), _translate("EVPY", "Battery Prediciton"))
        self.label_13.setText(_translate("EVPY", "Predict battery mass and size for a given duration and specific energy"))
        self.label_14.setText(_translate("EVPY", "\n"
"Time duration of mission or mission phase\n"
"\n"
"\n"
"Specific energy (energy/mass) of mission or mission phase\n"
"\n"
"(OPTIONAL)\n"
"The mass density (mass/volume) of a lipo battery"))
        self.pushButton_6.setText(_translate("EVPY", "Run"))
        self.label_43.setText(_translate("EVPY", "Hours"))
        self.label_44.setText(_translate("EVPY", "Wh/kg"))
        self.label_45.setText(_translate("EVPY", "kg/m^3"))
        self.label_56.setText(_translate("EVPY", "Mass of Required Battery Pack"))
        self.label_57.setText(_translate("EVPY", "Volume of Required Battery Pack"))
        self.label_58.setText(_translate("EVPY", "Kg"))
        self.label_59.setText(_translate("EVPY", "m^3"))
        self.sfBox.setTabText(self.sfBox.indexOf(self.tab_7), _translate("EVPY", "Battery Size"))
        self.actionPerformance.setText(_translate("EVPY", "Performance"))
        self.actionContour.setText(_translate("EVPY", "Contour"))
        self.actionSize.setText(_translate("EVPY", "Size"))
        self.actionPrediction.setText(_translate("EVPY", "Prediction"))
        self.actionSize_2.setText(_translate("EVPY", "Size"))
        self.actionLosses.setText(_translate("EVPY", "Losses"))
        self.actionSize_3.setText(_translate("EVPY", "Size"))

    def motor_pred(self):
    
            V = self.vBox.value()
            d = self.dBox.value()
            Rm = self.RmBox.value()
            kt = self.ktBox.value()
            IO = self.IOBox_2.value()
            
            kv = 60/(kt*2*np.pi) #[rpm/V]
    
               
            
            # generate speed range based on applied voltage
            V_app = d*V #[V]
            N_max = kv*V_app #[rpm]
            N_range = np.linspace(0,N_max,num=50) #[rpm]
            w_range = N_range*(np.pi/30.0) #[rad/s]
            
            # generate and plot predictions
            T,P_out,I_mot,P_mot,n_mot = ev.motor_pred(w_range, V, d, kt, Rm, IO)
            
            
            # plot results versus speed
            fig,ax = plt.subplots(1,3,sharex=True)
            for axis in ax:
                axis.set_xlabel("Rotational speed [rev/min]")
                axis.grid()
            
            # motor torque-speed
            ax[0].plot(N_range,T*1e3)
            ax[0].set_ylabel("Torque [N.m]")
            
            # motor output power
            ax[1].plot(N_range,P_out,label="Output")
            ax[1].set_ylabel("Power [W]")
            
            # efficiencies
            ax[2].plot(N_range,n_mot*100,'--',label="Motor")
            ax[2].set_ylabel("Efficiency [%]")
            ax[2].legend()
            
            plt.tight_layout()
            plt.show()
            
    def motor_efficiency(self):
        V0 = self.veff.value()
        kv = self.teff.value()
        Rm = self.reff.value()
        IO = self.ieff.value()
        kt = 60/(kv*2*np.pi) #[rpm/V]
        d = np.linspace(0.5, 1, 100)
        
        #V = np.linspace(0.5*V0, V0, 100)
        N_max = kv*V0
        N_range = np.linspace(0,N_max, num=100)
        w_range = N_range*(np.pi/30.0)
        #create torque values
        T_all = np.zeros((len(d),100))
        n_all = np.zeros((len(d), 100))
        I_all = np.zeros((len(d),100))
        
        #get values 
        for i in range(0, len(d)):
            T,P_out,I_mot,P_mot,n_mot = ev.motor_pred(w_range, V0, d[i], kt, Rm, IO)
            T_all[i] = T*1e3
            n_all[i] = n_mot
            I_all[i] = I_mot
            
        for i in range(0,len(d)):
            plt.scatter(N_range, T_all[i])
            plt.ylim(0,T_all[99][0])
            plt.show
            
        
        N1= N_range[0]
        N = self.neff.value()
        tu = self.toeff.value()
        
        #find closest x 
        for i in range(0, len(N_range)):
            if abs(N_range[i]- N) < abs(N1-N):
                N1 = N_range[i]
        #find poition of x 
        for i in range(0, len(w_range)):
            if N_range[i] == N1:
                xnum = i
        #find closest y at x 
        t1 = T_all[0][xnum]
        for i in range(0, len(d)):
            if abs(T_all[i][xnum] - tu) < abs((t1-tu)):
                t1 = T_all[i][xnum] 
        #find position of this y value 
        for i in range(0, len(d)):
            if T_all[i][xnum] == t1:
                ynum = i
                
        #efficency at point one 
        n1 = n_all[ynum][xnum]
        I1 = I_all[ynum][xnum]
                
        #Delete that Line and find the next point 
        T_all = np.delete(T_all, ynum, 0)
        #find closest y2 at x 
        t2 = T_all[0][xnum]
        for i in range(0, len(d)-1):
            if abs(T_all[i][xnum] - tu) < abs((t2-tu)):
                t2 = T_all[i][xnum]
                
        #find position of this y value 
        for i in range(0, len(d)-1):
            if T_all[i][xnum] == t2:
                ynum2 = i
        
        #efficency at point 2
        n2 = n_all[ynum2][xnum]
        I2 = I_all[ynum2][xnum]
        #interpolate to find npnt
        
        npnt = n1+(tu-t1)*((n2-n1)/(t2-t1))
        Ipnt = I1+(tu-t1)*((I2-I1)/(t2-t1))
        
        self.Ioutput.setValue(Ipnt)
        self.Noutput.setValue(npnt)
        print(npnt)
        print(Ipnt)
    
    def motor_contour(self):
        n = self.NBox.value()
        t = self.TBox_2.value()
        kt = self.KtBox.value()
        Rm = self.RmBox_2.value()
        IO = self.IOBox.value()
        num = int(self.numBox.value())
        N_array, T_array, n_array = ev.motor_contour(n, t, kt, Rm, IO, num)
        
        plt.contourf(N_array,T_array,n_array*100,cmap='jet')
        plt.colorbar()
        plt.xlabel('Speed [rev/min]')
        plt.ylabel('Torque [mN.m]')
        plt.title("Sample torque/speed/efficiency contour")
        plt.tight_layout()
        
        plt.show()
       
    def motor_size(self):
        t = self.T2Box.value()
        x = self.XBox.value()
        s = self.sBox.value()
        if s == 0:
            m_tot, U_tot, Do, Lo, km = ev.motor_size(t,x)
        else:
            m_tot, U_tot, Do, Lo, km = ev.motor_size(t,x, s)
    
      
        self.doubleSpinBox.setValue(m_tot)
        self.doubleSpinBox_3.setValue(U_tot)
        self.doubleSpinBox_4.setValue(Do)
        self.doubleSpinBox_5.setValue(Lo)
        self.doubleSpinBox_6.setValue(km)
    
    
    def esc_pred(self):
        im = self.ImBox.value()
        Pm = self.PmBox.value()
        v = self.VBox.value()
        d = self.dBox_2.value()
        f = self.fBox.value()
        Ron = self.RonBox.value()
        ton = self.TonBox.value()
        
        # sample specs of KDE 2304XF-2350 motor
        kv = 2350.0 #[rpm/V]
        P_range = np.linspace(0,Pm,num=50)
        I_range = np.linspace(0, im, num=50)
        
        
        # sample voltage from a 2S battery, 50% throttle
        V_batt = v
        d = d
        
        # generate speed range based on applied voltage
        V_app = V_batt*d #[V]
        N_max = kv*V_app #[rpm]
        N_range = np.linspace(0,N_max,num=50) #[rpm]
          
        
        # generate and plot predictions
        I_dc,P_dc,n_esc = ev.esc_pred(I_range ,P_range,V_batt,d, f, Ron, ton) 
           
        # plot results versus speed
        plt.plot(N_range,n_esc*100,'.-',label="ESC")
        plt.xlabel("Rotational speed [rev/min]")
        plt.grid()
        
        
        # efficiencies
        
        
        plt.ylabel("Efficiency [%]")
        
        
        plt.tight_layout()
        plt.show()
        
        
    def esc_size(self):
        p = self.doubleSpinBox_2.value()
        sf = self.doubleSpinBox_7.value()
        if sf ==0: 
             m, U = ev.esc_size(p)
        else:
             m, U = ev.esc_size(p,sf)
        self.doubleSpinBox_8.setValue(m)
        self.doubleSpinBox_9.setValue(U)
    
    
    def batt_pred(self):
        i = self.IBox.value()
        t = self.tBox.value()
        q = self.QBox.value()
        r = self.RBox.value()
        n = self.n_serBox.value() 
        nP = self.n_prllBox.value()
        pkrt = self.pkrtBox.value()
        
        #V_term,dod,soc =  ev.batt_pred(i, t, q, r, n, nP, pkrt)
        #print(V_term,dod,soc)
        if n == 0 :
            n = 1
        else:
            n = self.n_serBox.value() 
        if nP ==0:
            nP =1
        else:
             nP = self.n_prllBox.value()
        if pkrt == 0:
            pkrt = 1.2
        else:
            pkrt = self.pkrtBox.value()
        
        # create discharge test
        t = np.linspace(0,1.0,100) #[s], 1 hour sim
        I_amp = i
        I_cmd = I_amp*np.ones(t.shape) #[A] commanded current vector
        
           
        # compute only the voltage drop (ignoring DOD, SOC returned values)
        V_pred = ev.batt_pred(I_cmd,t,q,r,n, nP, pkrt)[0] #capture only first output
        
        # extract only time+data above 3.3 V
        y = V_pred[V_pred>3.3] #[V]
        x = t[V_pred>3.3]*60.0 #[min]
        
        batt_fig,batt_ax = plt.subplots(1,1)
        batt_ax.plot(x,y)
        batt_ax.set_xlabel("Time [min]")
        batt_ax.set_ylabel("Terminal voltage [V]")
        batt_fig.suptitle("Battery performance of 610 mAh battery at 2C discharge")
        batt_ax.grid(True)
        
        plt.show()
    
    def batt_size(self):
        t = self.tBox_2.value()
        e = self.eBox.value()
        rho = self.rhoBox.value()
        m,U = ev.batt_size(t, e, rho)
        
        self.doubleSpinBox_10.setValue(m)
        self.doubleSpinBox_11.setValue(U)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EVPY = QtWidgets.QMainWindow()
    ui = Ui_EVPY()
    ui.setupUi(EVPY)
    EVPY.show()
    sys.exit(app.exec_())
