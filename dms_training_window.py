# -*- coding: utf-8 -*-

# Form implementation goenerated from reading ui file 'dms_training_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
# Originally built for 1920 x 1160 screens

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import pyqtgraph as pg
import numpy as np
# from utilities import *
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, False)
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, False)

class Ui_trainingWindow:
    def __init__(self, MainWindow, opts, app):
        self.opts = opts
        ogscreen = np.array([1920, 1160])  # screen program was originally designed for
        ogsize = np.array([1500, 1000])  # original size of program

        screen = app.primaryScreen()
        # print('Screen: %s' % screen.name())
        screenSize = screen.size()
        screenSize = np.array([screenSize.width(), screenSize.height()])
        availableGeometry = screen.availableGeometry()
        availableGeometry = np.array([availableGeometry.width(), availableGeometry.height()])
        print('Screen Size:', screenSize)
        print('Available:', availableGeometry)

        self.scale = screenSize / ogscreen
        scale = self.scale
        print(scale)

        font = QtGui.QFont()
        # self.stdFont = self.trialNumLabel.font()
        print(f'default font: {font.pointSize()} pt, {font.pixelSize()} px')
        # font.setPointSize(14 * scale[1])
        # font.setPointSize(10)# * scale[1])
        # font.setPointSize(13)
        self.font = QtGui.QFont(font)

        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.boldfont = font

        MainWindow.setObjectName("MainWindow")
        x = min(ogsize[0], availableGeometry[0])
        y = min(ogsize[1], availableGeometry[1])
        MainWindow.resize(x, y)
        # MainWindow.resize(availableGeometry[0], availableGeometry[1])

        # MainWindow.setStyleSheet("QLabel {color: 'gray'; background-color: 'black'}")
        # MainWindow.setStyleSheet("QMainWindow {background: 'black';}")

        #   SEPARATOR LINES
        self.infoSeparatorLine1 = QtWidgets.QFrame()
        self.infoSeparatorLine1.setFrameShape(QtWidgets.QFrame.HLine)
        self.infoSeparatorLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.infoSeparatorLine1.setObjectName("infoSeparatorLine1")

        #   MENU BAR

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1792, 21))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")

        self.menu_View = QtWidgets.QMenu(self.menubar)
        self.menu_View.setObjectName("menu_View")

        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        heading = self.makeHeading()
        self.makeStatusGroup()
        self.makeControlsGroup()
        self.makePerformanceGroup()
        trialTimelineLayout = self.makeTrialTimelineLayout()
        motorLayout = self.makeMotorControlsLayout()

        # Final arrangement

        mainGUIGrid = QtWidgets.QGridLayout()
        mainGUIGrid.addWidget(self.currentStatusGroup, 0,0,10,1)
        mainGUIGrid.addWidget(self.controlsGroup, 0,1,10,1)
        mainGUIGrid.addWidget(self.performanceGroup, 0,2,7,1)
        # mainGUIGrid.addLayout(middleGUI, 0,1,2,1)
        mainGUIGrid.addLayout(trialTimelineLayout, 7,2,1,2)
        mainGUIGrid.addLayout(motorLayout, 0,3,2,1)
        mainGUIGrid.setColumnStretch(0,1)
        mainGUIGrid.setColumnStretch(1,1)
        mainGUIGrid.setColumnStretch(2,1)
        mainGUIGrid.setColumnStretch(3,0)
        mainGUIGrid.setRowStretch(0,1)
        mainGUIGrid.setRowStretch(1,1)
        mainGUIGrid.setRowStretch(2,1)
        mainGUIGrid.setRowStretch(3,1)
        mainGUIGrid.setRowStretch(4,1)
        mainGUIGrid.setRowStretch(5,1)
        mainGUIGrid.setRowStretch(6,1)
        mainGUIGrid.setRowStretch(7,1)
        mainGUIGrid.setRowStretch(8,1)
        mainGUIGrid.setRowStretch(9,1)

        space = max(y/ogsize[1], 0)

        fullGUI = QtWidgets.QVBoxLayout()
        fullGUI.addLayout(heading)
        fullGUI.addWidget(self.infoSeparatorLine1)
        fullGUI.addLayout(mainGUIGrid)
        # fullGUI.addLayout(mainGUI)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setObjectName("centralWidget")
        x = ogsize[0]
        y = ogsize[1]
        # x = min(ogsize[0], availableGeometry[0])
        # y = min(ogsize[1], availableGeometry[1])
        # centralWidget.setMaximumSize(ogsize[0], ogsize[1])
        centralWidget.setMaximumSize(x, y)
        # centralWidget.setMaximumSize(availableGeometry[0], availableGeometry[1])

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setObjectName("scrollArea")
        scrollArea.setBackgroundRole(QtGui.QPalette.Shadow)

        centralWidget.setLayout(fullGUI)
        scrollArea.setWidget(centralWidget)
        MainWindow.setCentralWidget(scrollArea)

        # self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.mainWindow = MainWindow

        # REDO SPACING for platform independence
    def makeHeading(self):
        scale = self.scale

        # LABELS #
        self.titleLabel = QtWidgets.QLabel("DMS TRAINING")
        # self.titleLabel.setGeometry(QtCore.QRect(10 * scale[0], 10 * scale[1], int(231 * scale[0]), int(41 * scale[1])))
        bigfont = QtGui.QFont()
        # bigfont.setPointSize(int(20 * scale[1]))
        bigfont.setPointSize(20)
        bigfont.setBold(True)
        bigfont.setWeight(75)
        self.titleLabel.setFont(bigfont)
        self.titleLabel.setObjectName("titleLabel")

        font = self.font
        boldfont = self.boldfont
        ps = font.pointSize()

        self.currentAnimalLabel = QtWidgets.QLabel("Current Animal")
        self.currentAnimalLabel.setFont(boldfont)
        self.currentAnimalLabel.setObjectName("currentAnimalLabel")

        self.currentPathLabel = QtWidgets.QLabel("Current Path")
        self.currentPathLabel.setFont(boldfont)
        self.currentPathLabel.setObjectName("currentPathLabel")

        # BUTTONS #
        self.startButton = QtWidgets.QPushButton("Run")
        self.startButton.setObjectName("startButton")
        self.startButton.setMinimumSize(ps * len("Run") * 4, ps * len("Run") * 2)

        self.changePathButton = QtWidgets.QPushButton("Change")
        self.changePathButton.setObjectName("changePathButton")

        self.backButton = QtWidgets.QPushButton("back")  # we don't even use this
        self.backButton.setObjectName("backButton")

        self.stopButton = QtWidgets.QPushButton("stop")
        self.stopButton.setObjectName("stopButton")

        #   LINE EDITS
        self.curAnimalLineEdit = QtWidgets.QLineEdit()
        self.curAnimalLineEdit.setObjectName("curAnimalLineEdit")

        self.curPathLineEdit = QtWidgets.QLineEdit()
        self.curPathLineEdit.setObjectName("curPathLineEdit")

        self.taskTypeComboBox = QtWidgets.QComboBox()
        self.taskTypeComboBox.setObjectName("taskTypeComboBox")
        self.taskTypeComboBox.addItem("Training")
        self.taskTypeComboBox.addItem("ITS")

        self.odorTypeComboBox = QtWidgets.QComboBox()
        self.odorTypeComboBox.setObjectName("odorTypeComboBox")
        self.odorTypeComboBox.addItem("AB/AB")
        self.odorTypeComboBox.addItem("CD/AB")

        curPathVBox = QtWidgets.QVBoxLayout()
        curPathVBox.addWidget(self.currentPathLabel)#, alignment=QtCore.Qt.AlignBottom)
        curPathVBox.addWidget(self.changePathButton)#, alignment=QtCore.Qt.AlignTop)
        curPathVBox.setSpacing(0)

        headingHBox = QtWidgets.QHBoxLayout()
        headingHBox.addWidget(self.titleLabel)
        headingHBox.addWidget(self.odorTypeComboBox)
        headingHBox.addWidget(self.taskTypeComboBox)
        headingHBox.addWidget(self.stopButton)
        headingHBox.addWidget(self.backButton)
        headingHBox.addWidget(self.startButton)
        headingHBox.addWidget(self.currentAnimalLabel)
        headingHBox.addWidget(self.curAnimalLineEdit)
        headingHBox.addWidget(self.backButton)
        headingHBox.addLayout(curPathVBox)
        headingHBox.addWidget(self.curPathLineEdit)
        return headingHBox

    def makeStatusGroup(self):
        scale = self.scale
        font = self.font
        boldfont = self.boldfont

        self.currentStatusGroup = QtWidgets.QGroupBox()
        self.currentStatusGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.currentStatusGroup.setObjectName("currentStatusGroup")
        self.currentStatusGroup.setTitle("Current Status")

        # Labels #
        self.trialNumLabel = QtWidgets.QLabel("Trial No.:")
        self.trialNumLabel.setObjectName("trialNumLabel")

        self.trialTypeLabel = QtWidgets.QLabel("Trial Type:")
        self.trialTypeLabel.setObjectName("trialTypeLabel")

        self.trialStructLabel = QtWidgets.QLabel("Trial Stucture:")
        self.trialStructLabel.setObjectName("trialStructLabel")

        self.lickIndicatorLabel = QtWidgets.QLabel("Lick Indicators")
        self.lickIndicatorLabel.setObjectName("lickIndicatorLabel")
        self.lickIndicatorLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.trialByTrialGraphicLabel = QtWidgets.QLabel("Trial-by-Trial Performance")
        self.trialByTrialGraphicLabel.setObjectName("trialByTrialGraphicLabel")

        self.correctGraphicLabel = QtWidgets.QLabel("Correct %")
        self.correctGraphicLabel.setObjectName("correctGraphicLabel")

        self.biasGraphicLabel = QtWidgets.QLabel("Bias")
        self.biasGraphicLabel.setObjectName("biasGraphicLabel")

        self.trialByTrialGraphicLabel.setFont(boldfont)
        self.correctGraphicLabel.setFont(boldfont)
        self.biasGraphicLabel.setFont(boldfont)

        # Text Browsers #
        self.trialTypeTextBrowser = QtWidgets.QTextBrowser()
        self.trialTypeTextBrowser.setObjectName("trialTypeTextBrowser")
        self.trialTypeTextBrowser.setMinimumSize(1, 1)  # need to reduce min size to make resizeable
        # self.trialTypeTextBrowser.setMaximumHeight(self.stdFontSize*3)

        self.trialStructTextBrowser = QtWidgets.QTextBrowser()
        self.trialStructTextBrowser.setObjectName("trialStructTextBrowser")
        self.trialStructTextBrowser.setMinimumSize(1, 1)
        # self.trialStructTextBrowser.setMinimumSize(1, 1)

        self.trialNoTextBrowser = QtWidgets.QTextBrowser()
        self.trialNoTextBrowser.setObjectName("trialNoTextBrowser")
        self.trialNoTextBrowser.setMinimumSize(1, 1)
        # self.trialNoTextBrowser.setMinimumSize(1, 1)

        # Widgets #
        self.leftLickIndicatorWidget = QtWidgets.QWidget()
        self.leftLickIndicatorWidget.setObjectName("leftLickIndicatorWidget")
        self.leftLickIndicatorWidget.setStyleSheet(
            "QWidget { background-color: %s}" % QtGui.QColor(0, 0, 0).name())

        self.rightLickIndicatorWidget = QtWidgets.QWidget()
        self.rightLickIndicatorWidget.setObjectName("rightLickIndicatorWidget")
        self.rightLickIndicatorWidget.setStyleSheet(
            "QWidget { background-color: %s}" % QtGui.QColor(0, 0, 0).name())

        x, y = np.array([60, 55]) #* scale
        self.leftLickIndicatorWidget.setMinimumSize(x, y)
        # self.leftLickIndicatorWidget.heightForWidth(60/50)
        self.rightLickIndicatorWidget.setMinimumSize(x, y)
        # self.rightLickIndicatorWidget.heightForWidth(60/50)
        x, y = np.array([60, 55]) #* scale
        self.rightLickIndicatorWidget.setMaximumSize(x, y)
        self.leftLickIndicatorWidget.setMaximumSize(x, y)

        # Was QtWidgets.QGraphicsView before pg.PlotWidget
        self.trialByTrialGraphic = pg.PlotWidget()
        self.trialByTrialGraphic.setObjectName("trialByTrialGraphic")

        self.correctTrialsGraphic = pg.PlotWidget()
        self.correctTrialsGraphic.setObjectName("correctTrialsGraphic")

        self.biasGraphic = pg.PlotWidget()
        self.biasGraphic.setObjectName("biasGraphic")

        # Layouts #
        statusGrid = QtWidgets.QGridLayout()
        
        statusGrid.addWidget(self.trialNumLabel, 0,0)
        statusGrid.addWidget(self.trialTypeLabel, 1,0)
        statusGrid.addWidget(self.trialStructLabel, 2,0)

        statusGrid.addWidget(self.trialNoTextBrowser, 0,1)
        statusGrid.addWidget(self.trialTypeTextBrowser, 1,1)
        statusGrid.addWidget(self.trialStructTextBrowser, 2,1)

        # statusGrid.setColumnStretch(0,1)
        # statusGrid.setColumnStretch(1,2)

        lickHBar = QtWidgets.QHBoxLayout()
        lickHBar.addWidget(self.leftLickIndicatorWidget)
        lickHBar.addWidget(self.rightLickIndicatorWidget)
        # lickHBar.insertSpacing(1, 20)
        # lickHBar.insertStretch(1, .3)

        lickVBar = QtWidgets.QVBoxLayout()
        lickVBar.addWidget(self.lickIndicatorLabel)
        lickVBar.addLayout(lickHBar)

        statusHBar = QtWidgets.QHBoxLayout()
        statusHBar.addLayout(statusGrid, 2)
        statusHBar.addLayout(lickVBar, 1)
        statusHBar.addStretch()

        statusVBar = QtWidgets.QVBoxLayout()
        statusVBar.addLayout(statusHBar, 3)
        statusVBar.addWidget(self.trialByTrialGraphicLabel)
        statusVBar.addWidget(self.trialByTrialGraphic, 5)
        statusVBar.addWidget(self.correctGraphicLabel)
        statusVBar.addWidget(self.correctTrialsGraphic, 5)
        statusVBar.addWidget(self.biasGraphicLabel)
        statusVBar.addWidget(self.biasGraphic, 4)

        self.currentStatusGroup.setLayout(statusVBar)

    def makeTrialStuctureLayout(self):
        scale = self.scale
        font = self.font
        boldfont = self.boldfont

        # LABELS #
        self.trialStructureLabel = QtWidgets.QLabel("Trial Structure")
        self.trialStructureLabel.setObjectName("trialStructureLabel")
        # self.trialStructureLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.trialStructureLabel.setFont(boldfont)

        self.automateLabel = QtWidgets.QLabel("Control Type")
        self.automateLabel.setObjectName("controlType")

        self.trialTypeControlLabel = QtWidgets.QLabel("Trial Types:")
        self.trialTypeControlLabel.setObjectName("trialTypeControlLabel")

        self.trialTimelineSelectionLabel = QtWidgets.QLabel("Trial Timeline Selection:")
        self.trialTimelineSelectionLabel.setObjectName("trialTimelineSelectionLabel")

        self.trialStructureControlLabel = QtWidgets.QLabel("Trial Structure")
        self.trialStructureControlLabel.setObjectName("trialStructureControlLabel")

        self.useUserProbLabel = QtWidgets.QLabel("Probability source")
        self.useUserProbLabel.setObjectName("useUserProbLabel")

        self.probabilityLabel = QtWidgets.QLabel("Probabilities")
        self.probabilityLabel.setObjectName("probabilityLabel")
        self.probabilityLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.automaticProbabilityLabel = QtWidgets.QLabel("Auto")
        self.automaticProbabilityLabel.setObjectName("automaticProbabilityLabel")
        self.automaticProbabilityLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.customProbabilityLabel = QtWidgets.QLabel("Custom")
        self.customProbabilityLabel.setObjectName("customProbabilityLabel")
        self.customProbabilityLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.aaProbabilityLabel = QtWidgets.QLabel("AA")
        self.aaProbabilityLabel.setObjectName("aaProbabilityLabel")

        self.abProbabilityLabel = QtWidgets.QLabel("AB")
        self.abProbabilityLabel.setObjectName("abProbabilityLabel")

        self.bbProbabilityLabel = QtWidgets.QLabel("BB")
        self.bbProbabilityLabel.setObjectName("bbProbabilityLabel")

        self.baProbabilityLabel = QtWidgets.QLabel("BA")
        self.baProbabilityLabel.setObjectName("baProbabilityLabel")

        font.setBold(False)
        font.setUnderline(False)
        self.automateLabel.setFont(font)
        self.trialTypeControlLabel.setFont(font)
        self.trialTimelineSelectionLabel.setFont(font)
        self.trialStructureControlLabel.setFont(font)
        self.useUserProbLabel.setFont(font)
        self.probabilityLabel.setFont(font)
        # self.automaticProbabilityLabel.setFont(font)
        # self.customProbabilityLabel.setFont(font)
        # self.aaProbabilityLabel.setFont(font)
        # self.abProbabilityLabel.setFont(font)
        # self.bbProbabilityLabel.setFont(font)
        # self.baProbabilityLabel.setFont(font)

        # COMBO BOXES #
        self.automateComboBox = QtWidgets.QComboBox()
        self.automateComboBox.setObjectName("automateComboBox")
        self.automateComboBox.addItem("Manual")
        self.automateComboBox.addItem("Automate")
        # self.automateComboBox.setMinimumSize(1, 1)

        self.trialStructureComboBox = QtWidgets.QComboBox()
        self.trialStructureComboBox.setObjectName("trialStructureComboBox")
        self.trialStructureComboBox.addItem("Alternating")
        self.trialStructureComboBox.addItem("Random")
        # self.trialStructureComboBox.setMinimumSize(1, 1)

        self.useUserProbComboBox = QtWidgets.QComboBox()
        self.useUserProbComboBox.setObjectName("trialStructureComboBox")
        self.useUserProbComboBox.addItem("Automatic")
        self.useUserProbComboBox.addItem("Custom")
        # self.useUserProbComboBox.setMinimumSize(1, 1)

        self.trialTypeComboBox = QtWidgets.QComboBox()
        self.trialTypeComboBox.setObjectName("trialTypeComboBox")
        self.trialTypeComboBox.addItem("Full")
        self.trialTypeComboBox.addItem("AA/AB")
        # self.trialTypeComboBox.setMinimumSize(1, 1)

        self.trialTimelineComboBox = QtWidgets.QComboBox()
        self.trialTimelineComboBox.setObjectName("trialTimelineComboBox")
        self.trialTimelineComboBox.addItem("Standard Structure")
        self.trialTimelineComboBox.addItem("Learning Structure")
        self.trialTimelineComboBox.addItem("Delay = 2000ms")
        # self.trialTimelineComboBox.setMinimumSize(1, 1)

        # LINE EDITS #
        self.aaProbabilityLineEdit = QtWidgets.QLineEdit()
        self.aaProbabilityLineEdit.setObjectName("aaProbabilityLineEdit")
        # self.aaProbabilityLineEdit.setMinimumSize(1, 1)

        self.bbProbabilityLineEdit = QtWidgets.QLineEdit()
        self.bbProbabilityLineEdit.setObjectName("bbProbabilityLineEdit")
        # self.bbProbabilityLineEdit.setMinimumSize(1, 1)

        self.abProbabilityLineEdit = QtWidgets.QLineEdit()
        self.abProbabilityLineEdit.setObjectName("abProbabilityLineEdit")
        # self.abProbabilityLineEdit.setMinimumSize(1, 1)

        # TEXT BROWSERS
        self.baCustomProbabilityTextBrowser = QtWidgets.QTextBrowser()
        self.baCustomProbabilityTextBrowser.setObjectName("baCustomProbabilityTextBrowser")
        self.baCustomProbabilityTextBrowser.setMinimumSize(1, 1)

        self.baProbabilityTextBrowser = QtWidgets.QTextBrowser()
        self.baProbabilityTextBrowser.setObjectName("baProbabilityTextBrowser")
        self.baProbabilityTextBrowser.setMinimumSize(1, 10)

        self.bbProbabilityTextBrowser = QtWidgets.QTextBrowser()
        self.bbProbabilityTextBrowser.setObjectName("bbProbabilityTextBrowser")
        self.bbProbabilityTextBrowser.setMinimumSize(1, 1)

        self.aaProbabilityTextBrowser = QtWidgets.QTextBrowser()
        self.aaProbabilityTextBrowser.setObjectName("aaProbabilityTextBrowser")
        self.aaProbabilityTextBrowser.setMinimumSize(1, 1)

        self.abProbabilityTextBrowser = QtWidgets.QTextBrowser()
        self.abProbabilityTextBrowser.setObjectName("abProbabilityTextBrowser")
        self.abProbabilityTextBrowser.setMinimumSize(1, 1)

        structureBoxGrid = QtWidgets.QGridLayout()
        structureBoxGrid.addWidget(self.automateLabel, 0, 0)
        structureBoxGrid.addWidget(self.automateComboBox, 1, 0)
        structureBoxGrid.addWidget(self.trialTypeControlLabel, 2, 0)
        structureBoxGrid.addWidget(self.trialTypeComboBox, 3, 0)
        structureBoxGrid.addWidget(self.trialTimelineSelectionLabel, 4, 0)
        structureBoxGrid.addWidget(self.trialTimelineComboBox, 5, 0)
        structureBoxGrid.addWidget(self.trialStructureControlLabel, 0, 1)
        structureBoxGrid.addWidget(self.trialStructureComboBox, 1, 1)
        structureBoxGrid.addWidget(self.useUserProbLabel, 2, 1)
        structureBoxGrid.addWidget(self.useUserProbComboBox, 3, 1)
        # structureBoxGrid.setSpacing(0)
        structureBoxGrid.setVerticalSpacing(0)
        structureBoxGrid.setHorizontalSpacing(5)

        probabilityGrid = QtWidgets.QGridLayout()
        probabilityGrid.addWidget(self.automaticProbabilityLabel, 0, 1)
        probabilityGrid.addWidget(self.aaProbabilityLabel, 1, 0)
        probabilityGrid.addWidget(self.abProbabilityLabel, 2, 0)
        probabilityGrid.addWidget(self.bbProbabilityLabel, 3, 0)
        probabilityGrid.addWidget(self.baProbabilityLabel, 4, 0)
        probabilityGrid.addWidget(self.customProbabilityLabel, 0, 2)
        probabilityGrid.addWidget(self.aaProbabilityTextBrowser, 1, 1)
        probabilityGrid.addWidget(self.abProbabilityTextBrowser, 2, 1)
        probabilityGrid.addWidget(self.bbProbabilityTextBrowser, 3, 1)
        probabilityGrid.addWidget(self.baProbabilityTextBrowser, 4, 1)
        probabilityGrid.addWidget(self.aaProbabilityLineEdit, 1, 2)
        probabilityGrid.addWidget(self.abProbabilityLineEdit, 2, 2)
        probabilityGrid.addWidget(self.bbProbabilityLineEdit, 3, 2)
        probabilityGrid.addWidget(self.baCustomProbabilityTextBrowser, 4, 2)
        probabilityGrid.setSpacing(0)
        # probabilityGrid.setHorizontalSpacing(5)
        # probabilityGrid.setVerticalSpacing(0)
        # probabilityGrid.setColumnStretch(0, 0)
        probabilityGrid.setColumnStretch(1, 1)
        probabilityGrid.setColumnStretch(2, 1)
        # c1_width = probabilityGrid.cellRect(1,1)
        # c2_width = probabilityGrid.cellRect(1,2)
        probVBox = QtWidgets.QVBoxLayout()
        probVBox.addWidget(self.probabilityLabel)
        probVBox.addLayout(probabilityGrid)

        trialStructureHBox = QtWidgets.QHBoxLayout()
        trialStructureHBox.addLayout(structureBoxGrid)
        trialStructureHBox.addLayout(probVBox)

        trialStructureLayout = QtWidgets.QVBoxLayout()
        trialStructureLayout.addWidget(self.trialStructureLabel)
        trialStructureLayout.addLayout(trialStructureHBox)
        # trialStructureLayout.addLayout(probabilityGrid)
        return trialStructureLayout

    def makeStimulusBoundsLayout(self):
        scale = self.scale
        font = self.font
        boldfont = self.boldfont

        # LABELS #
        self.stimulusBoundsLabel = QtWidgets.QLabel("Stimulus Bounds")
        self.stimulusBoundsLabel.setFont(boldfont)
        self.stimulusBoundsLabel.setObjectName("stimulusBoundsLabel")

        self.upperboundLabel = QtWidgets.QLabel("Upper\nBound")
        self.upperboundLabel.setObjectName("upperboundLabel")

        self.lowerboundLabel = QtWidgets.QLabel("Lower\nBound")
        self.lowerboundLabel.setObjectName("lowerboundLabel")

        self.aaStimulusLabel = QtWidgets.QLabel("AA")
        self.aaStimulusLabel.setObjectName("aaStimulusLabel")
        self.aaStimulusLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.abStimulusLabel = QtWidgets.QLabel("AB")
        self.abStimulusLabel.setObjectName("abStimulusLabel")
        self.abStimulusLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.bbStimulusLabel = QtWidgets.QLabel("BB")
        self.bbStimulusLabel.setObjectName("bbStimulusLabel")
        self.bbStimulusLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.baStimulusLabel = QtWidgets.QLabel("BA")
        self.baStimulusLabel.setObjectName("baStimulusLabel")
        self.baStimulusLabel.setAlignment(QtCore.Qt.AlignCenter)
        # self.baStimulusLabel.setMinimumSize(1, 1)

        # BUTTONS #
        self.upper3Button = QtWidgets.QPushButton()
        self.upper3Button.setText("All 3")
        self.upper3Button.setObjectName("upper3Button")
        # self.upper3Button.setFont(font)
        # self.upper3Button.setMinimumSize(1, 1)

        self.upper1Button = QtWidgets.QPushButton()
        self.upper1Button.setText("All 1")
        self.upper1Button.setObjectName("upper1Button")
        # self.upper1Button.setFont(font)
        # self.upper1Button.setMinimumSize(1, 1)

        self.lower3Button = QtWidgets.QPushButton()
        self.lower3Button.setText("All 3")
        self.lower3Button.setObjectName("lower3Button")
        # self.lower3Button.setFont(font)
        # self.lower3Button.setMinimumSize(1, 1)

        self.lower1Button = QtWidgets.QPushButton()
        self.lower1Button.setText("All 1")
        self.lower1Button.setObjectName("lower1Button")
        # self.lower1Button.setFont(font)
        # self.lower1Button.setMinimumSize(1, 1)

        # LINE EDITS #
        self.aaUpperLineEdit = QtWidgets.QLineEdit()
        self.aaUpperLineEdit.setObjectName("aaUpperLineEdit")

        self.baUpperLineEdit = QtWidgets.QLineEdit()
        self.baUpperLineEdit.setObjectName("baUpperLineEdit")

        self.bbUpperLineEdit = QtWidgets.QLineEdit()
        self.bbUpperLineEdit.setObjectName("bbUpperLineEdit")

        self.abUpperLineEdit = QtWidgets.QLineEdit()
        self.abUpperLineEdit.setObjectName("abUpperLineEdit")

        self.abLowerLineEdit = QtWidgets.QLineEdit()
        self.abLowerLineEdit.setObjectName("abLowerLineEdit")

        self.baLowerLineEdit = QtWidgets.QLineEdit()
        self.baLowerLineEdit.setObjectName("baLowerLineEdit")

        self.aaLowerLineEdit = QtWidgets.QLineEdit()
        self.aaLowerLineEdit.setObjectName("aaLowerLineEdit")

        self.bbLowerLineEdit = QtWidgets.QLineEdit()
        self.bbLowerLineEdit.setObjectName("bbLowerLineEdit")

        # LAYOUTS #

        stimulusGrid = QtWidgets.QGridLayout()
        stimulusGrid.addWidget(self.upper3Button, 1, 0)
        stimulusGrid.addWidget(self.upper1Button, 2, 0)
        stimulusGrid.addWidget(self.lower3Button, 3, 0)
        stimulusGrid.addWidget(self.lower1Button, 4, 0)
        stimulusGrid.addWidget(self.aaStimulusLabel, 0, 2)
        stimulusGrid.addWidget(self.abStimulusLabel, 0, 3)
        stimulusGrid.addWidget(self.bbStimulusLabel, 0, 4)
        stimulusGrid.addWidget(self.baStimulusLabel, 0, 5)
        stimulusGrid.addWidget(self.upperboundLabel, 1, 1, 2,1)
        stimulusGrid.addWidget(self.aaUpperLineEdit, 1, 2, 2,1)
        stimulusGrid.addWidget(self.abUpperLineEdit, 1, 3, 2,1)
        stimulusGrid.addWidget(self.bbUpperLineEdit, 1, 4, 2,1)
        stimulusGrid.addWidget(self.baUpperLineEdit, 1, 5, 2,1)
        stimulusGrid.addWidget(self.lowerboundLabel, 3, 1, 2,1)
        stimulusGrid.addWidget(self.aaLowerLineEdit, 3, 2, 2,1)
        stimulusGrid.addWidget(self.abLowerLineEdit, 3, 3, 2,1)
        stimulusGrid.addWidget(self.bbLowerLineEdit, 3, 4, 2,1)
        stimulusGrid.addWidget(self.baLowerLineEdit, 3, 5, 2,1)
        stimulusGrid.setVerticalSpacing(0)
        stimulusGrid.setHorizontalSpacing(5)

        stimulusVBox = QtWidgets.QVBoxLayout()
        stimulusVBox.addWidget(self.stimulusBoundsLabel)
        stimulusVBox.addLayout(stimulusGrid)
        stimulusVBox.setSpacing(0)
        return stimulusVBox

    def makeWaterLayout(self):
        scale = self.scale
        font = self.font
        boldfont = self.boldfont

        # LABELS #
        self.waterLabel = QtWidgets.QLabel("Water")
        self.waterLabel.setFont(boldfont)
        self.waterLabel.setObjectName("waterLabel")

        self.leftWaterTimeLabel = QtWidgets.QLabel("Left Water Time")
        self.leftWaterTimeLabel.setObjectName("leftWaterTimeLabel")
        self.leftWaterTimeLabel.setFont(font)

        self.rightWaterTimeLabel = QtWidgets.QLabel("Right Water Time")
        self.rightWaterTimeLabel.setObjectName("rightWaterTimeLabel")
        self.rightWaterTimeLabel.setFont(font)

        self.trialsToWaterLabel = QtWidgets.QLabel("Trials to water")
        self.trialsToWaterLabel.setObjectName("trialsToWaterLabel")
        self.trialsToWaterLabel.setFont(font)

        self.minLicksLabel = QtWidgets.QLabel("Min Licks")
        self.minLicksLabel.setObjectName("minLicksLabel")
        self.minLicksLabel.setFont(font)
        # self.minLicksLabel.setAlignment(QtCore.Qt.AlignBottom)

        self.earlyWaterLabel = QtWidgets.QLabel("Early")
        self.earlyWaterLabel.setObjectName("earlyWaterLabel")

        # BUTTONS #
        self.giveWaterToggle = QtWidgets.QPushButton("Give\nWater")
        self.giveWaterToggle.setObjectName("giveWaterButton")
        self.giveWaterToggle.setCheckable(True)
        self.giveWaterToggle.setFont(font)
        self.giveWaterToggle.setMinimumSize(0,0)

        self.increaseWaterButton = QtWidgets.QPushButton()
        self.increaseWaterButton.setText("+.2")
        self.increaseWaterButton.setObjectName("increaseWaterButton")
        # self.increaseWaterButton.setMinimumSize(1,1)

        self.decreaseWaterButton = QtWidgets.QPushButton()
        self.decreaseWaterButton.setText("-.2")
        self.decreaseWaterButton.setObjectName("decreaseWaterButton")
        # self.decreaseWaterButton.setMinimumSize(1,1)

        self.increaseEarlyWaterButton = QtWidgets.QPushButton()
        self.increaseEarlyWaterButton.setText("+.2")
        self.increaseEarlyWaterButton.setObjectName("increaseEarlyWaterButton")
        # self.increaseEarlyWaterButton.setMinimumSize(1,1)

        self.decreaseEarlyWaterButton = QtWidgets.QPushButton()
        self.decreaseEarlyWaterButton.setText("-.2")
        self.decreaseEarlyWaterButton.setObjectName("decreaseEarlyWaterButton")
        # self.decreaseEarlyWaterButton.setMinimumSize(1,1)

        # LINE EDITS #
        self.leftWaterAmountLineEdit = QtWidgets.QLineEdit()
        self.leftWaterAmountLineEdit.setObjectName("leftWaterAmountLineEdit")

        self.earlyLeftWaterAmountLineEdit = QtWidgets.QLineEdit()
        self.earlyLeftWaterAmountLineEdit.setObjectName("earlyLeftWaterAmountLineEdit")

        self.rightWaterAmountLineEdit = QtWidgets.QLineEdit()
        self.rightWaterAmountLineEdit.setObjectName("rightWaterAmountLineEdit")

        self.earlyRightWaterAmountLineEdit = QtWidgets.QLineEdit()
        self.earlyRightWaterAmountLineEdit.setObjectName("earlyRightWaterAmountLineEdit")

        self.trialsToWaterLineEdit = QtWidgets.QLineEdit()
        self.trialsToWaterLineEdit.setObjectName("trialsToWaterLineEdit")
        self.trialsToWaterLineEdit.setMaximumWidth(100*scale[0])

        self.minLicksLineEdit = QtWidgets.QLineEdit()
        self.minLicksLineEdit.setObjectName("minLicksLineEdit")
        self.minLicksLineEdit.setMaximumWidth(100*scale[0])
        # self.minLicksLineEdit.setAlignment(QtCore.Qt.AlignTop)

        # LAYOUTS #
        waterTimeGrid = QtWidgets.QGridLayout()
        waterTimeGrid.addWidget(self.increaseWaterButton, 1, 0)
        waterTimeGrid.addWidget(self.decreaseWaterButton, 2, 0)
        waterTimeGrid.addWidget(self.increaseEarlyWaterButton, 3, 0)
        waterTimeGrid.addWidget(self.decreaseEarlyWaterButton, 4, 0)
        waterTimeGrid.addWidget(self.leftWaterTimeLabel, 0, 2)
        waterTimeGrid.addWidget(self.rightWaterTimeLabel, 0, 3)
        waterTimeGrid.addWidget(self.leftWaterAmountLineEdit, 1, 2, 2, 1)
        waterTimeGrid.addWidget(self.rightWaterAmountLineEdit, 1, 3, 2, 1)
        waterTimeGrid.addWidget(self.earlyWaterLabel, 3, 1, 2, 1)
        waterTimeGrid.addWidget(self.earlyLeftWaterAmountLineEdit, 3, 2, 2, 1)
        waterTimeGrid.addWidget(self.earlyRightWaterAmountLineEdit, 3, 3, 2, 1)
        waterTimeGrid.setVerticalSpacing(0)
        waterTimeGrid.setHorizontalSpacing(5)
        
        waterLicksVBar = QtWidgets.QVBoxLayout()
        # waterLicksVBar.addWidget(self.earlyLickCheckToggle,2)
        waterLicksVBar.addWidget(self.giveWaterToggle)
        waterLicksVBar.addWidget(self.minLicksLabel, alignment=QtCore.Qt.AlignBottom)
        waterLicksVBar.addWidget(self.minLicksLineEdit, alignment=QtCore.Qt.AlignTop)
        waterLicksVBar.addWidget(self.trialsToWaterLabel, alignment=QtCore.Qt.AlignBottom)
        waterLicksVBar.addWidget(self.trialsToWaterLineEdit, alignment=QtCore.Qt.AlignTop)
        waterLicksVBar.setSpacing(5)

        # giveWaterHBar = QtWidgets.QHBoxLayout()
        # giveWaterHBar.addWidget(self.giveWaterToggle, alignment=QtCore.Qt.AlignLeft)
        # giveWaterHBar.addWidget(self.trialsToWaterLabel)
        # giveWaterHBar.addWidget(self.trialsToWaterLineEdit)
        # giveWaterHBar.insertSpacing(1, 5)
        # giveWaterHBar.insertSpacing(2, 5)

        waterDeliveryVBar = QtWidgets.QVBoxLayout()
        # waterDeliveryVBar.addLayout(giveWaterHBar)
        waterDeliveryVBar.addLayout(waterTimeGrid)
        waterDeliveryVBar.setAlignment(QtCore.Qt.AlignTop)
        # waterDeliveryVBar.setSpacing(0)

        waterOptsLayout = QtWidgets.QHBoxLayout()
        waterOptsLayout.addLayout(waterLicksVBar, 1)
        waterOptsLayout.addLayout(waterDeliveryVBar, 10)
        waterOptsLayout.setSpacing(0)

        waterLayout = QtWidgets.QVBoxLayout()
        waterLayout.addWidget(self.waterLabel)
        waterLayout.addLayout(waterOptsLayout)
        # waterLayout.setSpacing(0)
        return waterLayout

    def makeEarlyLickLayout(self):
        scale = self.scale
        font = self.font
        boldfont = self.boldfont

        # LABELS #
        self.earlyLickLabel = QtWidgets.QLabel("Early Lick")
        self.earlyLickLabel.setFont(boldfont)
        self.earlyLickLabel.setObjectName("earlyLickLabel")

        self.earlyLickPerformanceLabel = QtWidgets.QLabel("Early Lick %, Last 30 Trials")
        self.earlyLickPerformanceLabel.setFont(font)
        self.earlyLickPerformanceLabel.setObjectName("earlyLickPerformanceLabel")

        # BUTTONS #
        self.earlyLickCheckToggle = QtWidgets.QPushButton("Check Early \nLicks")
        self.earlyLickCheckToggle.setObjectName("earlyLickCheckToggle")
        self.earlyLickCheckToggle.setCheckable(True)
        self.earlyLickCheckToggle.setFont(font)
        ps = font.pointSize()
        self.earlyLickCheckToggle.setMaximumWidth(ps*10)
        # self.earlyLickCheckToggle.setMinimumHeight(ps*5)
        # self.earlyLickCheckToggle.setMinimumSize(ps*len("Check Early")*.7, ps*4)

        # GRAPHICS #
        self.earlyLickPerformanceGraphic = pg.PlotWidget()
        self.earlyLickPerformanceGraphic.setObjectName("earlyLickPerformanceGraphic")

        earlyLickPlotVBar = QtWidgets.QVBoxLayout()
        earlyLickPlotVBar.addWidget(self.earlyLickLabel)
        earlyLickPlotVBar.addWidget(self.earlyLickCheckToggle)
        earlyLickPlotVBar.addWidget(self.earlyLickPerformanceLabel)
        earlyLickPlotVBar.addWidget(self.earlyLickPerformanceGraphic)
        return earlyLickPlotVBar

    def makeControlsGroup(self):
        scale = self.scale

        self.controlsGroup = QtWidgets.QGroupBox()#self.centralwidget)
        # self.controlsGroup.setGeometry(QtCore.QRect(540*scale[0], 90*scale[1], 550*scale[0], 700*scale[1]))
        self.controlsGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.controlsGroup.setFlat(False)
        self.controlsGroup.setCheckable(False)
        self.controlsGroup.setObjectName("controlsGroup")
        self.controlsGroup.setTitle("Controls")

        self.controlsLine1 = QtWidgets.QFrame()
        self.controlsLine1.setFrameShape(QtWidgets.QFrame.HLine)
        self.controlsLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.controlsLine1.setObjectName("controlsLine1")

        self.controlsLine2 = QtWidgets.QFrame()
        self.controlsLine2.setFrameShape(QtWidgets.QFrame.HLine)
        self.controlsLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.controlsLine2.setObjectName("controlsLine2")

        self.controlsLine3 = QtWidgets.QFrame()
        self.controlsLine3.setFrameShape(QtWidgets.QFrame.HLine)
        self.controlsLine3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.controlsLine3.setObjectName("controlsLine3")

        trialStructureLayout = self.makeTrialStuctureLayout()
        stimulusBoundsLayout = self.makeStimulusBoundsLayout()
        waterLayout = self.makeWaterLayout()
        earlyLickLayout = self.makeEarlyLickLayout()

        controlsVBar = QtWidgets.QVBoxLayout()
        controlsVBar.addLayout(trialStructureLayout, 2)
        controlsVBar.addWidget(self.controlsLine1)
        controlsVBar.addLayout(stimulusBoundsLayout, 2)
        controlsVBar.addWidget(self.controlsLine2)
        controlsVBar.addLayout(waterLayout, 1)
        controlsVBar.addWidget(self.controlsLine3)
        controlsVBar.addLayout(earlyLickLayout)
        controlsVBar.setSpacing(10)

        self.controlsGroup.setLayout(controlsVBar)

    def makePerformanceGroup(self):
        scale = self.scale
        font = self.font
        boldfont = self.boldfont

        self.performanceGroup = QtWidgets.QGroupBox()#self.centralwidget)
        # self.performanceGroup.setGeometry(QtCore.QRect(1100 * scale[0], 90 * scale[1], 420 * scale[0], 500*scale[1]))
        self.performanceGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.performanceGroup.setObjectName("performanceGroup")
        self.performanceGroup.setTitle("Performance")

        # LABELS #
        self.overallPerformanceLabel = QtWidgets.QLabel("Overall Performance")
        self.overallPerformanceLabel.setFont(boldfont)
        self.overallPerformanceLabel.setObjectName("overallPerformanceLabel")

        self.trialTypePerformanceLabel = QtWidgets.QLabel("Trial Type Performance")
        self.trialTypePerformanceLabel.setFont(boldfont)
        self.trialTypePerformanceLabel.setObjectName("trialTypePerformanceLabel")

        self.earlyLickPerformanceLabel = QtWidgets.QLabel("Early Lick Performance")
        self.earlyLickPerformanceLabel.setFont(boldfont)
        self.earlyLickPerformanceLabel.setObjectName("trialTypePerformanceLabel")

        # TABLES #
        self.overallPerformanceTableWidget = QtWidgets.QTableWidget(self.performanceGroup)
        self.overallPerformanceTableWidget.setObjectName("overallPerformanceTableWidget")

        self.trialTypePerformanceTableWidget = QtWidgets.QTableWidget(self.performanceGroup)
        self.trialTypePerformanceTableWidget.setObjectName("trialTypePerformanceTableWidget")

        # LAYOUTS #
        perfVBar = QtWidgets.QVBoxLayout()
        overallPerfVBar = QtWidgets.QVBoxLayout()
        overallPerfVBar.addWidget(self.overallPerformanceLabel)
        overallPerfVBar.addWidget(self.overallPerformanceTableWidget)

        perfHBar = QtWidgets.QHBoxLayout()
        perfHBar.addLayout(overallPerfVBar)
        # perfHBar.addLayout(earlyLickPlotVBar)

        perfVBar.addLayout(perfHBar)
        perfVBar.addWidget(self.trialTypePerformanceLabel)
        perfVBar.addWidget(self.trialTypePerformanceTableWidget)

        self.performanceGroup.setLayout(perfVBar)

    def makeTrialTimelineLayout(self):
        scale = self.scale
        font = self.font
        boldfont = self.boldfont

        # LABELS #
        self.trialTimelineLabel = QtWidgets.QLabel("Trial Timeline")
        self.trialTimelineLabel.setFont(boldfont)
        self.trialTimelineLabel.setObjectName("trialTimelineLabel")

        self.itiLabel = QtWidgets.QLabel("Inter-trial\nInterval")
        self.itiLabel.setObjectName("itiLabel")
        self.itiLabel.setFont(font)

        self.odor1Label = QtWidgets.QLabel("1st Odor")
        self.odor1Label.setObjectName("odor1Label")
        self.odor1Label.setFont(font)

        self.Odor2Label = QtWidgets.QLabel("2nd Odor")
        self.Odor2Label.setObjectName("Odor2Label")
        self.Odor2Label.setFont(font)

        self.delay1Label = QtWidgets.QLabel("1st Delay")
        self.delay1Label.setObjectName("delay1Label")
        self.delay1Label.setFont(font)

        self.totalStimulusLabel = QtWidgets.QLabel("Total\nStimulus")
        self.totalStimulusLabel.setObjectName("totalStimulusLabel")
        self.totalStimulusLabel.setFont(font)

        self.noLickTimeLabel = QtWidgets.QLabel("No-Lick\nTime")
        self.noLickTimeLabel.setObjectName("noLickTimeLabel")
        self.noLickTimeLabel.setFont(font)

        self.consumptionTimeLabel = QtWidgets.QLabel("Consumption\nTime")
        self.consumptionTimeLabel.setObjectName("consumptionTimeLabel")
        self.consumptionTimeLabel.setFont(font)

        self.responseWindowLabel = QtWidgets.QLabel("Response\nWindow")
        self.responseWindowLabel.setObjectName("responseWindowLabel")
        self.responseWindowLabel.setFont(font)

        self.errorTOLabel = QtWidgets.QLabel("Error/Switch\nTO")
        self.errorTOLabel.setObjectName("errorTOLabel")
        self.errorTOLabel.setFont(font)

        self.earlyLickTOLabel = QtWidgets.QLabel("Early Lick\nTO")
        self.earlyLickTOLabel.setObjectName("earlyLickTOLabel")
        self.earlyLickTOLabel.setFont(font)

        self.earlyLickCheckTimeLabel = QtWidgets.QLabel("Early Lick\nCheck Time")
        self.earlyLickCheckTimeLabel.setObjectName("earlyLickCheckTimeLabel")
        self.earlyLickCheckTimeLabel.setFont(font)

        self.ITSDelayIncrementLabel = QtWidgets.QLabel("ITS Delay\nIncrement")
        self.ITSDelayIncrementLabel.setObjectName("ITSDelayIncrementLabel")
        self.ITSDelayIncrementLabel.setFont(font)

        self.ITSDelayDecrementLabel = QtWidgets.QLabel("ITS Delay\nDecrement")
        self.ITSDelayDecrementLabel.setObjectName("ITSDelayDecrementLabel")
        self.ITSDelayDecrementLabel.setFont(font)

        # TEXT BROWSERS #
        self.itiTextBrowser = QtWidgets.QTextBrowser()
        self.itiTextBrowser.setObjectName("itiTextBrowser")

        self.noLickTimeTextBrowser = QtWidgets.QTextBrowser()
        self.noLickTimeTextBrowser.setObjectName("noLickTimeTextBrowser")

        self.odor1TextBrowser = QtWidgets.QTextBrowser()
        self.odor1TextBrowser.setObjectName("odor1TextBrowser")

        self.delay1TextBrowser = QtWidgets.QTextBrowser()
        self.delay1TextBrowser.setObjectName("delay1TextBrowser")

        self.odor2TextBrowser = QtWidgets.QTextBrowser()
        self.odor2TextBrowser.setObjectName("odor2TextBrowser")

        self.responseWindowTextBrowser = QtWidgets.QTextBrowser()
        self.responseWindowTextBrowser.setObjectName("responseWindowTextBrowser")

        self.totalStimulusTextBrowser = QtWidgets.QTextBrowser()
        self.totalStimulusTextBrowser.setObjectName("totalStimulusTextBrowser")

        # LINE EDITS #
        self.itiLineEdit = QtWidgets.QLineEdit()
        self.itiLineEdit.setObjectName("itiLineEdit")

        self.errorTOLineEdit = QtWidgets.QLineEdit()
        self.errorTOLineEdit.setObjectName("errorTOLineEdit")

        self.earlyLickTOLineEdit = QtWidgets.QLineEdit()
        self.earlyLickTOLineEdit.setObjectName("earlyLickTOLineEdit")

        self.earlyLickCheckTimeLineEdit = QtWidgets.QLineEdit()
        self.earlyLickCheckTimeLineEdit.setObjectName("earlyLickCheckTimeLineEdit")

        self.ITSDelayDecrementLineEdit = QtWidgets.QLineEdit()
        self.ITSDelayDecrementLineEdit.setObjectName("ITSDelayDecrementLineEdit")

        self.ITSDelayIncrementLineEdit = QtWidgets.QLineEdit()
        self.ITSDelayIncrementLineEdit.setObjectName("ITSDelayIncrementLineEdit")

        self.noLickTimeLineEdit = QtWidgets.QLineEdit()
        self.noLickTimeLineEdit.setObjectName("noLickTimeLineEdit")

        self.odor1LineEdit = QtWidgets.QLineEdit()
        self.odor1LineEdit.setObjectName("odor1LineEdit")

        self.responseWindowLineEdit = QtWidgets.QLineEdit()
        self.responseWindowLineEdit.setObjectName("responseWindowLineEdit")

        self.delay1LineEdit = QtWidgets.QLineEdit()
        self.delay1LineEdit.setObjectName("delay1LineEdit")

        self.odor2LineEdit = QtWidgets.QLineEdit()
        self.odor2LineEdit.setObjectName("odor2LineEdit")

        self.consumptionTimeLineEdit = QtWidgets.QLineEdit()
        self.consumptionTimeLineEdit.setObjectName("consumptionTimeLineEdit")

        trialTimelineGrid = QtWidgets.QGridLayout()
        trialTimelineGrid.addWidget(self.itiLabel, 0, 0)
        trialTimelineGrid.addWidget(self.noLickTimeLabel, 0, 1)
        trialTimelineGrid.addWidget(self.odor1Label, 0, 2)
        trialTimelineGrid.addWidget(self.delay1Label, 0, 3)
        trialTimelineGrid.addWidget(self.Odor2Label, 0, 4)
        trialTimelineGrid.addWidget(self.responseWindowLabel, 0, 5)
        trialTimelineGrid.addWidget(self.totalStimulusLabel, 0, 6)
        trialTimelineGrid.addWidget(self.itiTextBrowser, 1, 0)
        trialTimelineGrid.addWidget(self.noLickTimeTextBrowser, 1, 1)
        trialTimelineGrid.addWidget(self.odor1TextBrowser, 1, 2)
        trialTimelineGrid.addWidget(self.delay1TextBrowser, 1, 3)
        trialTimelineGrid.addWidget(self.odor2TextBrowser, 1, 4)
        trialTimelineGrid.addWidget(self.responseWindowTextBrowser, 1, 5)
        trialTimelineGrid.addWidget(self.totalStimulusTextBrowser, 1, 6)
        trialTimelineGrid.addWidget(self.itiLineEdit, 2, 0)
        trialTimelineGrid.addWidget(self.noLickTimeLineEdit, 2, 1)
        trialTimelineGrid.addWidget(self.odor1LineEdit, 2, 2)
        trialTimelineGrid.addWidget(self.delay1LineEdit, 2, 3)
        trialTimelineGrid.addWidget(self.odor2LineEdit, 2, 4)
        trialTimelineGrid.addWidget(self.responseWindowLineEdit, 2, 5)
        trialTimelineGrid.addWidget(self.errorTOLabel, 3, 0)
        trialTimelineGrid.addWidget(self.ITSDelayDecrementLabel, 3, 2)
        trialTimelineGrid.addWidget(self.consumptionTimeLabel, 3, 5)
        trialTimelineGrid.addWidget(self.errorTOLineEdit, 4, 0)
        trialTimelineGrid.addWidget(self.ITSDelayDecrementLineEdit, 4, 2)
        trialTimelineGrid.addWidget(self.consumptionTimeLineEdit, 4, 5)
        trialTimelineGrid.addWidget(self.earlyLickTOLabel, 5, 0)
        trialTimelineGrid.addWidget(self.earlyLickCheckTimeLabel, 5, 1)
        trialTimelineGrid.addWidget(self.ITSDelayIncrementLabel, 5, 2)
        trialTimelineGrid.addWidget(self.earlyLickTOLineEdit, 6, 0)
        trialTimelineGrid.addWidget(self.earlyLickCheckTimeLineEdit, 6, 1)
        trialTimelineGrid.addWidget(self.ITSDelayIncrementLineEdit, 6, 2)
        # trialTimelineGrid.setSpacing(20)
        # trialTimelineGrid.setRowStretch(0,0)
        # trialTimelineGrid.setRowStretch(1,1)
        # trialTimelineGrid.setRowStretch(2,1)
        # trialTimelineGrid.setRowStretch(3,0)
        # trialTimelineGrid.setRowStretch(4,1)
        # trialTimelineGrid.setRowStretch(5,0)
        # trialTimelineGrid.setRowStretch(6,1)
        # trialTimelineGrid.setColumnStretch(0, 0)
        # trialTimelineGrid.setColumnStretch(1, 0)
        # trialTimelineGrid.setColumnStretch(2, 0)
        # trialTimelineGrid.setColumnStretch(3, 0)
        # trialTimelineGrid.setColumnStretch(4, 0)
        # trialTimelineGrid.setColumnStretch(5, 0)
        # trialTimelineGrid.setColumnStretch(6, 0)

        trialTimelineVBox = QtWidgets.QVBoxLayout()
        trialTimelineVBox.addWidget(self.trialTimelineLabel)
        trialTimelineVBox.addLayout(trialTimelineGrid)
        return trialTimelineVBox

    def makeMotorControlsLayout(self):
        font = self.font

        # LABELS #
        self.fastMotorLabel = QtWidgets.QLabel("Fast Motor")
        self.fastMotorLabel.setObjectName("fastMotorLabel")

        self.fastMotorSpeedLabel = QtWidgets.QLabel("Speed")
        self.fastMotorSpeedLabel.setObjectName("fastMotorSpeedLabel")
        self.fastMotorSpeedLabel.setFont(font)

        self.fastMotorStepLabel = QtWidgets.QLabel("Step Size")
        self.fastMotorStepLabel.setObjectName("fastMotorStepLabel")
        self.fastMotorStepLabel.setFont(font)

        self.slowMotorLabel = QtWidgets.QLabel("Slow Motor")
        self.slowMotorLabel.setObjectName("slowMotorLabel")

        self.slowMotorSpeedLabel = QtWidgets.QLabel("Speed")
        self.slowMotorSpeedLabel.setObjectName("slowMotorSpeedLabel")
        self.slowMotorSpeedLabel.setFont(font)

        self.slowMotorStepLabel = QtWidgets.QLabel("Step Size")
        self.slowMotorStepLabel.setObjectName("slowMotorStepLabel")
        self.slowMotorStepLabel.setFont(font)

        # LINE EDITS #
        L = len("Speed") * font.pointSize()
        self.fastMotorStepLineEdit = QtWidgets.QLineEdit()
        self.fastMotorStepLineEdit.setObjectName("fastMotorStepLineEdit")
        self.fastMotorStepLineEdit.setMinimumWidth(1)
        self.fastMotorStepLineEdit.setMaximumWidth(L)

        self.fastMotorSpeedLineEdit = QtWidgets.QLineEdit()
        self.fastMotorSpeedLineEdit.setObjectName("fastMotorSpeedLineEdit")
        self.fastMotorSpeedLineEdit.setMinimumWidth(1)
        self.fastMotorSpeedLineEdit.setMaximumWidth(L)
        # self.fastMotorSpeedLineEdit.setMaximumSize(10,10)

        self.slowMotorStepLineEdit = QtWidgets.QLineEdit()
        self.slowMotorStepLineEdit.setObjectName("slowMotorStepLineEdit")
        self.slowMotorStepLineEdit.setMinimumWidth(1)
        self.slowMotorStepLineEdit.setMaximumWidth(L)
        # self.slowMotorStepLineEdit.setMaximumSize(10,10)


        self.slowMotorSpeedLineEdit = QtWidgets.QLineEdit()
        self.slowMotorSpeedLineEdit.setObjectName("slowMotorSpeedLineEdit")
        self.slowMotorSpeedLineEdit.setMinimumWidth(1)
        self.slowMotorSpeedLineEdit.setMaximumWidth(L)
        # self.slowMotorSpeedLineEdit.setMaximumSize(10,10)

        # COMBO BOXES #
        self.movingPortComboBox = QtWidgets.QComboBox()
        self.movingPortComboBox.setObjectName("movingPortComboBox")
        self.movingPortComboBox.addItem("Moving Ports")
        self.movingPortComboBox.addItem("Stationary Ports")
        self.movingPortComboBox.setFont(font)
        pointSize = font.pointSize()
        self.movingPortComboBox.setMinimumWidth(pointSize * len("Moving Ports"))
        self.movingPortComboBox.setMaximumWidth(pointSize * len("Stationary Ports"))

        self.movingLRPortComboBox = QtWidgets.QComboBox()
        self.movingLRPortComboBox.setObjectName("movingLRPortComboBox")
        self.movingLRPortComboBox.addItem("Moving Ports")
        self.movingLRPortComboBox.addItem("Stationary Ports")
        self.movingLRPortComboBox.setFont(font)
        self.movingLRPortComboBox.setMinimumWidth(pointSize * len("Moving Ports"))
        self.movingLRPortComboBox.setMaximumWidth(pointSize * len("Stationary Ports"))

        # LAYOUTS #
        motorGrid = QtWidgets.QGridLayout()
        motorGrid.addWidget(self.fastMotorLabel, 0,0,1,2)
        motorGrid.addWidget(self.movingPortComboBox, 1,0,1,2)
        motorGrid.addWidget(self.fastMotorSpeedLabel, 2,0)
        motorGrid.addWidget(self.fastMotorStepLabel, 2,1)
        motorGrid.addWidget(self.fastMotorSpeedLineEdit, 3,0)
        motorGrid.addWidget(self.fastMotorStepLineEdit, 3,1)
        motorGrid.addWidget(self.slowMotorLabel, 4,0,1,2)
        motorGrid.addWidget(self.movingLRPortComboBox, 5,0,1,2)
        motorGrid.addWidget(self.slowMotorSpeedLabel, 6, 0)
        motorGrid.addWidget(self.slowMotorStepLabel, 6, 1)
        motorGrid.addWidget(self.slowMotorSpeedLineEdit, 7,0)
        motorGrid.addWidget(self.slowMotorStepLineEdit, 7, 1)
        motorGrid.setSpacing(2)
        return motorGrid


    #   SET TEXTS
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titleLabel.setText(_translate("MainWindow", "DMS TRAINING"))
        self.currentStatusGroup.setTitle(_translate("MainWindow", "Current Status"))
        self.lickIndicatorLabel.setText(_translate("MainWindow", "Lick Indicators"))
        self.trialNumLabel.setText(_translate("MainWindow", "Trial No.:"))
        self.trialTypeLabel.setText(_translate("MainWindow", "Trial Type:"))
        self.trialStructLabel.setText(_translate("MainWindow", "Trial Structure:"))
        self.trialByTrialGraphicLabel.setText(_translate("MainWindow", "Trial-by-Trial Performance"))
        self.correctGraphicLabel.setText(_translate("MainWindow", "Correct %"))
        self.biasGraphicLabel.setText(_translate("MainWindow", "Bias"))
        self.startButton.setText(_translate("MainWindow", "Run"))
        self.performanceGroup.setTitle(_translate("MainWindow", "Performance"))
        self.overallPerformanceLabel.setText(_translate("MainWindow", "Overall Performance"))
        self.trialTypePerformanceLabel.setText(_translate("MainWindow", "Trial Type Performance"))
        self.controlsGroup.setTitle(_translate("MainWindow", "Controls"))
        self.waterLabel.setText(_translate("MainWindow", "Water"))
        self.giveWaterToggle.setText(_translate("MainWindow", "Give Water"))
        self.earlyLickCheckToggle.setText(_translate("MainWindow", "Check Early Licks"))
        self.leftWaterTimeLabel.setText(_translate("MainWindow", "Left water time"))
        self.rightWaterTimeLabel.setText(_translate("MainWindow", "Right water time"))
        self.trialsToWaterLabel.setText(_translate("MainWindow", "Trials to water"))
        self.upperboundLabel.setText(_translate("MainWindow", "Upper Bound:"))
        self.lowerboundLabel.setText(_translate("MainWindow", "Lower Bound:"))
        self.trialStructureComboBox.setItemText(0, _translate("MainWindow", "Alternating"))
        self.trialStructureComboBox.setItemText(1, _translate("MainWindow", "Random"))
        self.trialStructureControlLabel.setText(_translate("MainWindow", "Trial Structure:"))
        self.trialTypeComboBox.setItemText(0, _translate("MainWindow", "Full"))
        self.trialTypeComboBox.setItemText(1, _translate("MainWindow", "AA/AB"))
        self.trialTypeControlLabel.setText(_translate("MainWindow", "Trial Types:"))
        self.trialTimelineComboBox.setItemText(0, _translate("MainWindow", "Standard Structure"))
        self.trialTimelineComboBox.setItemText(1, _translate("MainWindow", "Learning Structure"))
        self.trialTimelineComboBox.setItemText(2, _translate("MainWindow", "Delay = 2000ms"))
        self.trialTimelineSelectionLabel.setText(_translate("MainWindow", "Trial Timeline Selection:"))
        self.minLicksLabel.setText(_translate("MainWindow", "Minimum Licks:"))
        self.earlyWaterLabel.setText(_translate("MainWindow", "Early Water"))
        self.stimulusBoundsLabel.setText(_translate("MainWindow", "Stimulus Bounds"))
        self.trialStructureLabel.setText(_translate("MainWindow", "Trial Structure"))
        self.changePathButton.setText(_translate("MainWindow", "change"))
        self.backButton.setText(_translate("MainWindow", "back"))
        self.stopButton.setText(_translate("MainWindow", "stop"))
        self.itiLabel.setText(_translate("MainWindow", "Intertrial Interval"))
        self.odor1Label.setText(_translate("MainWindow", "1st Odor"))
        self.Odor2Label.setText(_translate("MainWindow", "2nd Odor"))
        self.delay1Label.setText(_translate("MainWindow", "1st Delay"))
        self.totalStimulusLabel.setText(_translate("MainWindow", "Total Stimulus"))
        self.noLickTimeLabel.setText(_translate("MainWindow", "No-Lick Time"))
        self.consumptionTimeLabel.setText(_translate("MainWindow", "Consumption Time"))
        self.responseWindowLabel.setText(_translate("MainWindow", "Response Window"))
        self.errorTOLabel.setText(_translate("MainWindow", "Error/Switch TO"))
        self.earlyLickTOLabel.setText(_translate("MainWindow", "Early Lick TO"))
        self.earlyLickCheckTimeLabel.setText(_translate("MainWindow", "Early Lick Check Time"))
        self.ITSDelayIncrementLabel.setText(_translate("MainWindow", "ITS Delay Increment"))
        self.ITSDelayDecrementLabel.setText(_translate("MainWindow", "ITS Delay Decrement"))
        self.trialTimelineLabel.setText(_translate("MainWindow", "Trial Timeline"))
        self.currentAnimalLabel.setText(_translate("MainWindow", "Current Animal:"))
        self.currentPathLabel.setText(_translate("MainWindow", "Current Path:"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menu_View.setTitle(_translate("MainWindow", "&View"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.automaticProbabilityLabel.setText(_translate("MainWindow", "Automatic"))
        self.customProbabilityLabel.setText(_translate("MainWindow", "Custom"))
        self.probabilityLabel.setText(_translate("MainWindow", "Probabilities"))
        self.useUserProbComboBox.setItemText(0, _translate("MainWindow", "Automatic"))
        self.useUserProbComboBox.setItemText(1, _translate("MainWindow", "Custom"))
        self.useUserProbLabel.setText(_translate("MainWindow", "Probability source"))
        self.automateComboBox.setItemText(0, _translate("MainWindow", "Manual"))
        self.automateComboBox.setItemText(1, _translate("MainWindow", "Automate"))
        self.automateLabel.setText(_translate("MainWindow", "Control Type"))
        self.taskTypeComboBox.setItemText(0, _translate("MainWindow", "Training"))
        self.taskTypeComboBox.setItemText(1, _translate("MainWindow", "ITS"))
        self.odorTypeComboBox.setItemText(0, _translate("MainWindow", "CD/AB"))
        self.odorTypeComboBox.setItemText(1, _translate("MainWindow", "AB/AB"))
        self.movingPortComboBox.setItemText(0, _translate("MainWindow", "Moving Ports"))
        self.movingPortComboBox.setItemText(1, _translate("MainWindow", "Stationary Ports"))
        self.movingLRPortComboBox.setItemText(0, _translate("MainWindow", "Moving Ports"))
        self.movingLRPortComboBox.setItemText(1, _translate("MainWindow", "Stationary Ports"))
        self.fastMotorLabel.setText(_translate("MainWindow", "Fast Motor"))
        self.fastMotorSpeedLabel.setText(_translate("MainWindow", "Speed"))
        self.fastMotorStepLabel.setText(_translate("MainWindow", "Step Size"))
        self.slowMotorLabel.setText(_translate("MainWindow", "Slow Motor (ITS)"))
        self.slowMotorSpeedLabel.setText(_translate("MainWindow", "Speed"))
        self.slowMotorStepLabel.setText(_translate("MainWindow", "Step Size"))
        self.upper3Button.setText(_translate("MainWindow", "All 3"))
        self.upper1Button.setText(_translate("MainWindow", "All 1"))
        self.lower3Button.setText(_translate("MainWindow", "All 3"))
        self.lower1Button.setText(_translate("MainWindow", "All 1"))

    def setOdorLabels(self):
        # _translate = QtCore.QCoreApplication.translate
        if self.opts.cd_ab:
            self.aaProbabilityLabel.setText("CA")
            self.abProbabilityLabel.setText("CB")
            self.bbProbabilityLabel.setText("DB")
            self.baProbabilityLabel.setText("DA")
            self.trialTypeComboBox.setItemText(1, "CA/CB")
            # self.stimulusLabel.setText(_translate("MainWindow", "CA               CB                DB               DA"))
        else:
            self.aaProbabilityLabel.setText("AA")
            self.abProbabilityLabel.setText("AB")
            self.bbProbabilityLabel.setText("BB")
            self.baProbabilityLabel.setText("BA")
            self.trialTypeComboBox.setItemText(1, "AA/AB")
            # self.stimulusLabel.setText(_translate("MainWindow", "AA               AB                BB               BA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    opts = None
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_trainingWindow(MainWindow, opts, app)
    ui.mainWindow.show()
    sys.exit(app.exec_())

