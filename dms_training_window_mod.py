# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dms_training_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class Ui_trainingWindow:
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1792, 1040)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(10, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")

        # MainWindow.setStyleSheet("QLabel {color: 'gray'; background-color: 'black'}")
        # MainWindow.setStyleSheet("QMainWindow {background: 'black';}")

#    GROUPS
        self.currentStatusGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.currentStatusGroup.setGeometry(QtCore.QRect(10, 90, 501, 871))
        self.currentStatusGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.currentStatusGroup.setObjectName("currentStatusGroup")

        self.performanceGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.performanceGroup.setGeometry(QtCore.QRect(960, 90, 421, 541))
        self.performanceGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.performanceGroup.setObjectName("performanceGroup")

        self.controlsGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.controlsGroup.setGeometry(QtCore.QRect(540, 90, 391, 576))
        self.controlsGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.controlsGroup.setFlat(False)
        self.controlsGroup.setCheckable(False)
        self.controlsGroup.setObjectName("controlsGroup")

#   TEXT BROWSERS
        self.trialTypeTextBrowser = QtWidgets.QTextBrowser(self.currentStatusGroup)
        self.trialTypeTextBrowser.setGeometry(QtCore.QRect(130, 60, 111, 31))
        self.trialTypeTextBrowser.setObjectName("trialTypeTextBrowser")

        self.trialStructTextBrowser = QtWidgets.QTextBrowser(self.currentStatusGroup)
        self.trialStructTextBrowser.setGeometry(QtCore.QRect(130, 100, 111, 31))
        self.trialStructTextBrowser.setObjectName("trialStructTextBrowser")

        self.trialNoTextBrowser = QtWidgets.QTextBrowser(self.currentStatusGroup)
        self.trialNoTextBrowser.setGeometry(QtCore.QRect(130, 20, 111, 31))
        self.trialNoTextBrowser.setObjectName("trialNoTextBrowser")

        self.itiTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.itiTextBrowser.setGeometry(QtCore.QRect(550, 720, 111, 41))
        self.itiTextBrowser.setObjectName("itiTextBrowser")

        self.noLickTimeTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.noLickTimeTextBrowser.setGeometry(QtCore.QRect(670, 720, 111, 41))
        self.noLickTimeTextBrowser.setObjectName("noLickTimeTextBrowser")

        self.odor1TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.odor1TextBrowser.setGeometry(QtCore.QRect(790, 720, 111, 41))
        self.odor1TextBrowser.setObjectName("odor1TextBrowser")

        self.delay1TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.delay1TextBrowser.setGeometry(QtCore.QRect(910, 720, 111, 41))
        self.delay1TextBrowser.setObjectName("delay1TextBrowser")

        self.odor2TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.odor2TextBrowser.setGeometry(QtCore.QRect(1030, 720, 111, 41))
        self.odor2TextBrowser.setObjectName("odor2TextBrowser")

        self.responseWindowTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.responseWindowTextBrowser.setGeometry(QtCore.QRect(1150, 720, 111, 41))
        self.responseWindowTextBrowser.setObjectName("responseWindowTextBrowser")

        self.totalStimulusTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.totalStimulusTextBrowser.setGeometry(QtCore.QRect(1270, 720, 111, 41))
        self.totalStimulusTextBrowser.setObjectName("totalStimulusTextBrowser")

        self.baCustomProbabilityTextBrowser = QtWidgets.QTextBrowser(self.controlsGroup)
        self.baCustomProbabilityTextBrowser.setGeometry(QtCore.QRect(330, 170, 41, 31))
        self.baCustomProbabilityTextBrowser.setObjectName("baCustomProbabilityTextBrowser")

        self.bbProbabilityTextBrowser = QtWidgets.QTextBrowser(self.controlsGroup)
        self.bbProbabilityTextBrowser.setGeometry(QtCore.QRect(270, 170, 41, 31))
        self.bbProbabilityTextBrowser.setObjectName("bbProbabilityTextBrowser")

        self.aaProbabilityTextBrowser = QtWidgets.QTextBrowser(self.controlsGroup)
        self.aaProbabilityTextBrowser.setGeometry(QtCore.QRect(270, 80, 41, 31))
        self.aaProbabilityTextBrowser.setObjectName("aaProbabilityTextBrowser")

        self.abProbabilityTextBrowser = QtWidgets.QTextBrowser(self.controlsGroup)
        self.abProbabilityTextBrowser.setGeometry(QtCore.QRect(270, 110, 41, 31))
        self.abProbabilityTextBrowser.setObjectName("abProbabilityTextBrowser")

        self.baProbabilityTextBrowser = QtWidgets.QTextBrowser(self.controlsGroup)
        self.baProbabilityTextBrowser.setGeometry(QtCore.QRect(270, 140, 41, 31))
        self.baProbabilityTextBrowser.setObjectName("baProbabilityTextBrowser")

#   GRAPHICS
        self.leftLickIndicatorWidget = QtWidgets.QWidget(self.currentStatusGroup)
        self.leftLickIndicatorWidget.setGeometry(QtCore.QRect(290, 50, 61, 51))
        self.leftLickIndicatorWidget.setObjectName("leftLickIndicatorWidget")

        self.rightLickIndicatorWidget = QtWidgets.QWidget(self.currentStatusGroup)
        self.rightLickIndicatorWidget.setGeometry(QtCore.QRect(370, 50, 61, 51))
        self.rightLickIndicatorWidget.setObjectName("rightLickIndicatorWidget")

        # Was QtWidgets.QGraphicsView before pg.PlotWidget
        self.trialByTrialGraphic = pg.PlotWidget(self.currentStatusGroup)
        self.trialByTrialGraphic.setGeometry(QtCore.QRect(40, 170, 431, 241))
        self.trialByTrialGraphic.setObjectName("trialByTrialGraphic")

        self.correctTrialsGraphic = pg.PlotWidget(self.currentStatusGroup)
        self.correctTrialsGraphic.setGeometry(QtCore.QRect(40, 440, 431, 221))
        self.correctTrialsGraphic.setObjectName("correctTrialsGraphic")

        self.biasGraphic = pg.PlotWidget(self.currentStatusGroup)
        self.biasGraphic.setGeometry(QtCore.QRect(100, 690, 311, 171))
        self.biasGraphic.setObjectName("biasGraphic")

        self.trialByTrialGraphicLabel = QtWidgets.QLabel(self.currentStatusGroup)
        self.trialByTrialGraphicLabel.setGeometry(QtCore.QRect(170, 140, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.trialByTrialGraphicLabel.setFont(font)
        self.trialByTrialGraphicLabel.setObjectName("trialByTrialGraphicLabel")

        self.correctGraphicLabel = QtWidgets.QLabel(self.currentStatusGroup)
        self.correctGraphicLabel.setGeometry(QtCore.QRect(220, 410, 68, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.correctGraphicLabel.setFont(font)
        self.correctGraphicLabel.setObjectName("correctGraphicLabel")

        self.biasGraphicLabel = QtWidgets.QLabel(self.currentStatusGroup)
        self.biasGraphicLabel.setGeometry(QtCore.QRect(240, 660, 68, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.biasGraphicLabel.setFont(font)
        self.biasGraphicLabel.setObjectName("biasGraphicLabel")

#   BUTTONS
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(680, 10, 211, 51))
        self.startButton.setObjectName("startButton")

        self.giveWaterButton = QtWidgets.QPushButton(self.controlsGroup)
        self.giveWaterButton.setGeometry(QtCore.QRect(190, 430, 112, 34))
        self.giveWaterButton.setObjectName("giveWaterButton")

        # self.changeAnimalButton = QtWidgets.QPushButton(self.centralwidget)
        # self.changeAnimalButton.setGeometry(QtCore.QRect(900, 40, 51, 21))
        # self.changeAnimalButton.setObjectName("changeAnimalButton")

        self.changePathButton = QtWidgets.QPushButton(self.centralwidget)
        self.changePathButton.setGeometry(QtCore.QRect(1100, 40, 51, 21))
        self.changePathButton.setObjectName("changePathButton")

        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(590, 20, 71, 31))
        self.backButton.setObjectName("backButton")

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(500, 20, 71, 31))
        self.stopButton.setObjectName("stopButton")

        self.earlyLickCheckToggle = QtWidgets.QPushButton(self.controlsGroup)
        self.earlyLickCheckToggle.setGeometry(QtCore.QRect(10, 420, 100, 31))
        self.earlyLickCheckToggle.setObjectName("earlyLickCheckToggle")
        self.earlyLickCheckToggle.setCheckable(True)

#   TABLES
        self.overallPerformanceTableWidget = QtWidgets.QTableWidget(self.performanceGroup)
        self.overallPerformanceTableWidget.setGeometry(QtCore.QRect(120, 40, 201, 211))
        self.overallPerformanceTableWidget.setObjectName("overallPerformanceTableWidget")

        self.trialTypePerformanceTableWidget = QtWidgets.QTableWidget(self.performanceGroup)
        self.trialTypePerformanceTableWidget.setGeometry(QtCore.QRect(10, 330, 541, 192))
        self.trialTypePerformanceTableWidget.setObjectName("trialTypePerformanceTableWidget")

#   LINE EDITS
        self.leftWaterAmountLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.leftWaterAmountLineEdit.setGeometry(QtCore.QRect(130, 490, 91, 31))
        self.leftWaterAmountLineEdit.setObjectName("leftWaterAmountLineEdit")

        self.earlyLeftWaterAmountLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.earlyLeftWaterAmountLineEdit.setGeometry(QtCore.QRect(130, 530, 91, 31))
        self.earlyLeftWaterAmountLineEdit.setObjectName("earlyLeftWaterAmountLineEdit")

        self.rightWaterAmountLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.rightWaterAmountLineEdit.setGeometry(QtCore.QRect(270, 490, 91, 31))
        self.rightWaterAmountLineEdit.setObjectName("rightWaterAmountLineEdit")

        self.earlyRightWaterAmountLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.earlyRightWaterAmountLineEdit.setGeometry(QtCore.QRect(270, 530, 91, 31))
        self.earlyRightWaterAmountLineEdit.setObjectName("earlyRightWaterAmountLineEdit")

        self.minLicksLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.minLicksLineEdit.setGeometry(QtCore.QRect(30, 480, 51, 31))
        self.minLicksLineEdit.setObjectName("minLicksLineEdit")

        self.aaUpperLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.aaUpperLineEdit.setGeometry(QtCore.QRect(140, 280, 51, 31))
        self.aaUpperLineEdit.setObjectName("aaUpperLineEdit")

        self.baUpperLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.baUpperLineEdit.setGeometry(QtCore.QRect(320, 280, 51, 31))
        self.baUpperLineEdit.setObjectName("baUpperLineEdit")

        self.bbUpperLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.bbUpperLineEdit.setGeometry(QtCore.QRect(260, 280, 51, 31))
        self.bbUpperLineEdit.setObjectName("bbUpperLineEdit")

        self.abUpperLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.abUpperLineEdit.setGeometry(QtCore.QRect(200, 280, 51, 31))
        self.abUpperLineEdit.setObjectName("abUpperLineEdit")

        self.abLowerLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.abLowerLineEdit.setGeometry(QtCore.QRect(200, 330, 51, 31))
        self.abLowerLineEdit.setObjectName("abLowerLineEdit")

        self.baLowerLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.baLowerLineEdit.setGeometry(QtCore.QRect(320, 330, 51, 31))
        self.baLowerLineEdit.setObjectName("baLowerLineEdit")

        self.aaLowerLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.aaLowerLineEdit.setGeometry(QtCore.QRect(140, 330, 51, 31))
        self.aaLowerLineEdit.setObjectName("aaLowerLineEdit")

        self.bbLowerLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.bbLowerLineEdit.setGeometry(QtCore.QRect(260, 330, 51, 31))
        self.bbLowerLineEdit.setObjectName("bbLowerLineEdit")

        self.curAnimalLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.curAnimalLineEdit.setGeometry(QtCore.QRect(1010, 20, 81, 31))
        self.curAnimalLineEdit.setObjectName("curAnimalLineEdit")

        self.curPathLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.curPathLineEdit.setGeometry(QtCore.QRect(1200, 20, 311, 31))
        self.curPathLineEdit.setObjectName("curPathLineEdit")

        self.itiLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.itiLineEdit.setGeometry(QtCore.QRect(570, 770, 71, 31))
        self.itiLineEdit.setObjectName("itiLineEdit")

        self.errorTOLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.errorTOLineEdit.setGeometry(QtCore.QRect(570, 840, 71, 31))
        self.errorTOLineEdit.setObjectName("errorTOLineEdit")

        self.earlyLickTOLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.earlyLickTOLineEdit.setGeometry(QtCore.QRect(570, 900, 71, 31))
        self.earlyLickTOLineEdit.setObjectName("earlyLickTOLineEdit")

        self.earlyLickCheckTimeLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.earlyLickCheckTimeLineEdit.setGeometry(QtCore.QRect(690, 900, 71, 31))
        self.earlyLickCheckTimeLineEdit.setObjectName("earlyLickCheckTimeLineEdit")

        self.ITSDelayDecrementLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ITSDelayDecrementLineEdit.setGeometry(QtCore.QRect(810, 840, 71, 31))
        self.ITSDelayDecrementLineEdit.setObjectName("ITSDelayDecrementLineEdit")

        self.ITSDelayIncrementLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ITSDelayIncrementLineEdit.setGeometry(QtCore.QRect(810, 900, 71, 31))
        self.ITSDelayIncrementLineEdit.setObjectName("ITSDelayIncrementLineEdit")

        self.noLickTimeLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.noLickTimeLineEdit.setGeometry(QtCore.QRect(690, 770, 71, 31))
        self.noLickTimeLineEdit.setObjectName("noLickTimeLineEdit")

        self.odor1LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.odor1LineEdit.setGeometry(QtCore.QRect(810, 770, 71, 31))
        self.odor1LineEdit.setObjectName("odor1LineEdit")

        self.responseWindowLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.responseWindowLineEdit.setGeometry(QtCore.QRect(1170, 770, 71, 31))
        self.responseWindowLineEdit.setObjectName("responseWindowLineEdit")

        self.delay1LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.delay1LineEdit.setGeometry(QtCore.QRect(930, 770, 71, 31))
        self.delay1LineEdit.setObjectName("delay1LineEdit")

        self.odor2LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.odor2LineEdit.setGeometry(QtCore.QRect(1050, 770, 71, 31))
        self.odor2LineEdit.setObjectName("odor2LineEdit")

        self.consumptionTimeLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.consumptionTimeLineEdit.setGeometry(QtCore.QRect(1170, 840, 71, 31))
        self.consumptionTimeLineEdit.setObjectName("consumptionTimeLineEdit")

        self.aaProbabilityLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.aaProbabilityLineEdit.setGeometry(QtCore.QRect(330, 80, 41, 31))
        self.aaProbabilityLineEdit.setObjectName("aaProbabilityLineEdit")

        self.bbProbabilityLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.bbProbabilityLineEdit.setGeometry(QtCore.QRect(330, 140, 41, 31))
        self.bbProbabilityLineEdit.setObjectName("bbProbabilityLineEdit")

        self.abProbabilityLineEdit = QtWidgets.QLineEdit(self.controlsGroup)
        self.abProbabilityLineEdit.setGeometry(QtCore.QRect(330, 110, 41, 31))
        self.abProbabilityLineEdit.setObjectName("abProbabilityLineEdit")

#   COMBO BOX/DROP DOWN LISTS
        self.automateComboBox = QtWidgets.QComboBox(self.controlsGroup)
        self.automateComboBox.setGeometry(QtCore.QRect(10, 30, 91, 31))
        self.automateComboBox.setObjectName("automateComboBox")
        self.automateComboBox.addItem("")
        self.automateComboBox.addItem("")

        self.trialStructureComboBox = QtWidgets.QComboBox(self.controlsGroup)
        self.trialStructureComboBox.setGeometry(QtCore.QRect(140, 100, 91, 31))
        self.trialStructureComboBox.setObjectName("trialStructureComboBox")
        self.trialStructureComboBox.addItem("")
        self.trialStructureComboBox.addItem("")

        self.useUserProbComboBox = QtWidgets.QComboBox(self.controlsGroup)
        self.useUserProbComboBox.setGeometry(QtCore.QRect(140, 170, 91, 31))
        self.useUserProbComboBox.setObjectName("trialStructureComboBox")
        self.useUserProbComboBox.addItem("")
        self.useUserProbComboBox.addItem("")

        self.trialTypeComboBox = QtWidgets.QComboBox(self.controlsGroup)
        self.trialTypeComboBox.setGeometry(QtCore.QRect(10, 100, 81, 31))
        self.trialTypeComboBox.setObjectName("trialTypeComboBox")
        self.trialTypeComboBox.addItem("")
        self.trialTypeComboBox.addItem("")

        self.trialTimelineComboBox = QtWidgets.QComboBox(self.controlsGroup)
        self.trialTimelineComboBox.setGeometry(QtCore.QRect(10, 170, 121, 31))
        self.trialTimelineComboBox.setObjectName("trialTimelineComboBox")
        self.trialTimelineComboBox.addItem("")
        self.trialTimelineComboBox.addItem("")
        self.trialTimelineComboBox.addItem("")

        self.taskTypeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.taskTypeComboBox.setGeometry(QtCore.QRect(400, 20, 91, 31))
        self.taskTypeComboBox.setObjectName("taskTypeComboBox")
        self.taskTypeComboBox.addItem("")
        self.taskTypeComboBox.addItem("")

#   LABELS
        self.lickIndicatorLabel = QtWidgets.QLabel(self.currentStatusGroup)
        self.lickIndicatorLabel.setGeometry(QtCore.QRect(330, 20, 111, 21))
        self.lickIndicatorLabel.setObjectName("lickIndicatorLabel")

        self.trialNumLabel = QtWidgets.QLabel(self.currentStatusGroup)
        self.trialNumLabel.setGeometry(QtCore.QRect(10, 30, 91, 21))
        self.trialNumLabel.setObjectName("trialNumLabel")

        self.trialTypeLabel = QtWidgets.QLabel(self.currentStatusGroup)
        self.trialTypeLabel.setGeometry(QtCore.QRect(10, 70, 81, 21))
        self.trialTypeLabel.setObjectName("trialTypeLabel")

        self.trialStructLabel = QtWidgets.QLabel(self.currentStatusGroup)
        self.trialStructLabel.setGeometry(QtCore.QRect(10, 110, 111, 21))
        self.trialStructLabel.setObjectName("trialStructLabel")

        self.waterLabel = QtWidgets.QLabel(self.controlsGroup)
        self.waterLabel.setGeometry(QtCore.QRect(160, 400, 68, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.waterLabel.setFont(font)
        self.waterLabel.setObjectName("waterLabel")

        self.overallPerformanceLabel = QtWidgets.QLabel(self.performanceGroup)
        self.overallPerformanceLabel.setGeometry(QtCore.QRect(130, 10, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.overallPerformanceLabel.setFont(font)
        self.overallPerformanceLabel.setObjectName("overallPerformanceLabel")

        self.trialTypePerformanceLabel = QtWidgets.QLabel(self.performanceGroup)
        self.trialTypePerformanceLabel.setGeometry(QtCore.QRect(130, 300, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.trialTypePerformanceLabel.setFont(font)
        self.trialTypePerformanceLabel.setObjectName("trialTypePerformanceLabel")

        self.upperboundLabel = QtWidgets.QLabel(self.controlsGroup)
        self.upperboundLabel.setGeometry(QtCore.QRect(50, 280, 81, 31))
        self.upperboundLabel.setObjectName("upperboundLabel")

        self.lowerboundLabel = QtWidgets.QLabel(self.controlsGroup)
        self.lowerboundLabel.setGeometry(QtCore.QRect(50, 330, 81, 31))
        self.lowerboundLabel.setObjectName("lowerboundLabel")

        self.stimulusLabel = QtWidgets.QLabel(self.controlsGroup)
        self.stimulusLabel.setGeometry(QtCore.QRect(160, 260, 211, 20))
        self.stimulusLabel.setObjectName("stimulusLabel")

        self.leftWaterTimeLabel = QtWidgets.QLabel(self.controlsGroup)
        self.leftWaterTimeLabel.setGeometry(QtCore.QRect(140, 460, 91, 31))
        self.leftWaterTimeLabel.setObjectName("leftWaterTimeLabel")

        self.rightWaterTimeLabel = QtWidgets.QLabel(self.controlsGroup)
        self.rightWaterTimeLabel.setGeometry(QtCore.QRect(280, 460, 81, 31))
        self.rightWaterTimeLabel.setObjectName("rightWaterTimeLabel")

        self.automateLabel = QtWidgets.QLabel(self.controlsGroup)
        self.automateLabel.setGeometry(QtCore.QRect(10, 5, 91, 31))
        self.automateLabel.setObjectName("controlType")

        self.useUserProbLabel = QtWidgets.QLabel(self.controlsGroup)
        self.useUserProbLabel.setGeometry(QtCore.QRect(140, 140, 91, 31))
        self.useUserProbLabel.setObjectName("useUserProbLabel")

        self.trialStructureControlLabel = QtWidgets.QLabel(self.controlsGroup)
        self.trialStructureControlLabel.setGeometry(QtCore.QRect(140, 70, 81, 21))
        self.trialStructureControlLabel.setObjectName("trialStructureControlLabel")

        self.trialTypeControlLabel = QtWidgets.QLabel(self.controlsGroup)
        self.trialTypeControlLabel.setGeometry(QtCore.QRect(10, 70, 91, 21))
        self.trialTypeControlLabel.setObjectName("trialTypeControlLabel")

        self.trialTimelineSelectionLabel = QtWidgets.QLabel(self.controlsGroup)
        self.trialTimelineSelectionLabel.setGeometry(QtCore.QRect(10, 140, 121, 31))
        self.trialTimelineSelectionLabel.setObjectName("trialTimelineSelectionLabel")

        self.minLicksLabel = QtWidgets.QLabel(self.controlsGroup)
        self.minLicksLabel.setGeometry(QtCore.QRect(20, 450, 71, 31))
        self.minLicksLabel.setObjectName("minLicksLabel")

        self.earlyWaterLabel = QtWidgets.QLabel(self.controlsGroup)
        self.earlyWaterLabel.setGeometry(QtCore.QRect(60, 530, 71, 31))
        self.earlyWaterLabel.setObjectName("earlyWaterLabel")

        self.stimulusBoundsLabel = QtWidgets.QLabel(self.controlsGroup)
        self.stimulusBoundsLabel.setGeometry(QtCore.QRect(130, 230, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.stimulusBoundsLabel.setFont(font)
        self.stimulusBoundsLabel.setObjectName("stimulusBoundsLabel")

        self.trialStructureLabel = QtWidgets.QLabel(self.controlsGroup)
        self.trialStructureLabel.setGeometry(QtCore.QRect(140, 20, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.trialStructureLabel.setFont(font)
        self.trialStructureLabel.setObjectName("trialStructureLabel")

        self.itiLabel = QtWidgets.QLabel(self.centralwidget)
        self.itiLabel.setGeometry(QtCore.QRect(560, 699, 91, 21))
        self.itiLabel.setObjectName("itiLabel")

        self.odor1Label = QtWidgets.QLabel(self.centralwidget)
        self.odor1Label.setGeometry(QtCore.QRect(820, 700, 71, 21))
        self.odor1Label.setObjectName("odor1Label")

        self.Odor2Label = QtWidgets.QLabel(self.centralwidget)
        self.Odor2Label.setGeometry(QtCore.QRect(1060, 700, 61, 21))
        self.Odor2Label.setObjectName("Odor2Label")

        self.delay1Label = QtWidgets.QLabel(self.centralwidget)
        self.delay1Label.setGeometry(QtCore.QRect(940, 700, 71, 21))
        self.delay1Label.setObjectName("delay1Label")

        self.totalStimulusLabel = QtWidgets.QLabel(self.centralwidget)
        self.totalStimulusLabel.setGeometry(QtCore.QRect(1290, 700, 91, 21))
        self.totalStimulusLabel.setObjectName("totalStimulusLabel")

        self.noLickTimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.noLickTimeLabel.setGeometry(QtCore.QRect(690, 700, 91, 21))
        self.noLickTimeLabel.setObjectName("noLickTimeLabel")

        self.consumptionTimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.consumptionTimeLabel.setGeometry(QtCore.QRect(1160, 820, 91, 21))
        self.consumptionTimeLabel.setObjectName("consumptionTimeLabel")

        self.responseWindowLabel = QtWidgets.QLabel(self.centralwidget)
        self.responseWindowLabel.setGeometry(QtCore.QRect(1160, 700, 101, 21))
        self.responseWindowLabel.setObjectName("responseWindowLabel")

        self.errorTOLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorTOLabel.setGeometry(QtCore.QRect(570, 820, 91, 21))
        self.errorTOLabel.setObjectName("errorTOLabel")

        self.earlyLickTOLabel = QtWidgets.QLabel(self.centralwidget)
        self.earlyLickTOLabel.setGeometry(QtCore.QRect(570, 870, 71, 41))
        self.earlyLickTOLabel.setObjectName("earlyLickTOLabel")

        self.earlyLickCheckTimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.earlyLickCheckTimeLabel.setGeometry(QtCore.QRect(690, 870, 100, 41))
        self.earlyLickCheckTimeLabel.setObjectName("earlyLickCheckTimeLabel")

        self.ITSDelayIncrementLabel = QtWidgets.QLabel(self.centralwidget)
        self.ITSDelayIncrementLabel.setGeometry(QtCore.QRect(810, 870, 100, 41))
        self.ITSDelayIncrementLabel.setObjectName("ITSDelayIncrementLabel")

        self.ITSDelayDecrementLabel = QtWidgets.QLabel(self.centralwidget)
        self.ITSDelayDecrementLabel.setGeometry(QtCore.QRect(810, 810, 100, 41))
        self.ITSDelayDecrementLabel.setObjectName("ITSDelayDecrementLabel")

        self.trialTimelineLabel = QtWidgets.QLabel(self.centralwidget)
        self.trialTimelineLabel.setGeometry(QtCore.QRect(890, 660, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.trialTimelineLabel.setFont(font)
        self.trialTimelineLabel.setObjectName("trialTimelineLabel")

        self.currentAnimalLabel = QtWidgets.QLabel(self.centralwidget)
        self.currentAnimalLabel.setGeometry(QtCore.QRect(900, 5, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.currentAnimalLabel.setFont(font)
        self.currentAnimalLabel.setObjectName("currentAnimalLabel")

        self.currentPathLabel = QtWidgets.QLabel(self.centralwidget)
        self.currentPathLabel.setGeometry(QtCore.QRect(1100, 5, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.currentPathLabel.setFont(font)
        self.currentPathLabel.setObjectName("currentPathLabel")

        self.probabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.probabilityLabel.setGeometry(QtCore.QRect(290, 30, 141, 25))
        self.probabilityLabel.setObjectName("probabilityLabel")

        self.automaticProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.automaticProbabilityLabel.setGeometry(QtCore.QRect(270, 60, 51, 25))
        self.automaticProbabilityLabel.setObjectName("automaticProbabilityLabel")

        self.customProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.customProbabilityLabel.setGeometry(QtCore.QRect(330, 60, 51, 25))
        self.customProbabilityLabel.setObjectName("customProbabilityLabel")

        self.aaProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.aaProbabilityLabel.setGeometry(QtCore.QRect(250, 80, 21, 31))
        self.aaProbabilityLabel.setObjectName("aaProbabilityLabel")

        self.abProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.abProbabilityLabel.setGeometry(QtCore.QRect(250, 110, 21, 31))
        self.abProbabilityLabel.setObjectName("abProbabilityLabel")

        self.bbProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.bbProbabilityLabel.setGeometry(QtCore.QRect(250, 140, 21, 31))
        self.bbProbabilityLabel.setObjectName("bbProbabilityLabel")

        self.baProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.baProbabilityLabel.setGeometry(QtCore.QRect(250, 170, 21, 31))
        self.baProbabilityLabel.setObjectName("baProbabilityLabel")

        self.aaProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.aaProbabilityLabel.setGeometry(QtCore.QRect(250, 80, 21, 31))
        self.aaProbabilityLabel.setObjectName("aaProbabilityLabel")

        self.abProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.abProbabilityLabel.setGeometry(QtCore.QRect(250, 110, 21, 31))
        self.abProbabilityLabel.setObjectName("abProbabilityLabel")

        self.bbProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.bbProbabilityLabel.setGeometry(QtCore.QRect(250, 140, 21, 31))
        self.bbProbabilityLabel.setObjectName("bbProbabilityLabel")

        self.baProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.baProbabilityLabel.setGeometry(QtCore.QRect(250, 170, 21, 31))
        self.baProbabilityLabel.setObjectName("baProbabilityLabel")

        self.probabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.probabilityLabel.setGeometry(QtCore.QRect(290, 30, 141, 25))
        self.probabilityLabel.setObjectName("probabilityLabel")

        self.automaticProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.automaticProbabilityLabel.setGeometry(QtCore.QRect(270, 60, 51, 25))
        self.automaticProbabilityLabel.setObjectName("automaticProbabilityLabel")

        self.customProbabilityLabel = QtWidgets.QLabel(self.controlsGroup)
        self.customProbabilityLabel.setGeometry(QtCore.QRect(330, 60, 51, 25))
        self.customProbabilityLabel.setObjectName("customProbabilityLabel")

#   SEPARATOR LINES
        self.controlsLine1 = QtWidgets.QFrame(self.controlsGroup)
        self.controlsLine1.setGeometry(QtCore.QRect(40, 210, 341, 20))
        self.controlsLine1.setFrameShape(QtWidgets.QFrame.HLine)
        self.controlsLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.controlsLine1.setObjectName("controlsLine1")

        self.controlsLine2 = QtWidgets.QFrame(self.controlsGroup)
        self.controlsLine2.setGeometry(QtCore.QRect(40, 380, 341, 20))
        self.controlsLine2.setFrameShape(QtWidgets.QFrame.HLine)
        self.controlsLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.controlsLine2.setObjectName("controlsLine2")

        self.infoSeparatorLine1 = QtWidgets.QFrame(self.centralwidget)
        self.infoSeparatorLine1.setGeometry(QtCore.QRect(37, 60, 1471, 20))
        self.infoSeparatorLine1.setFrameShape(QtWidgets.QFrame.HLine)
        self.infoSeparatorLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.infoSeparatorLine1.setObjectName("infoSeparatorLine1")

#   MENU BAR
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1792, 21))
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


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.mainWindow = MainWindow

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
        self.giveWaterButton.setText(_translate("MainWindow", "Give Water"))
        self.earlyLickCheckToggle.setText(_translate("MainWindow", "Check Early Licks"))
        self.leftWaterTimeLabel.setText(_translate("MainWindow", "Left water time"))
        self.rightWaterTimeLabel.setText(_translate("MainWindow", "Right water time"))
        self.upperboundLabel.setText(_translate("MainWindow", "Upper Bound:"))
        self.lowerboundLabel.setText(_translate("MainWindow", "Lower Bound:"))
        self.stimulusLabel.setText(_translate("MainWindow", "AA               AB                BB               BA"))
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
        self.aaProbabilityLabel.setText(_translate("MainWindow", "AA"))
        self.abProbabilityLabel.setText(_translate("MainWindow", "AB"))
        self.bbProbabilityLabel.setText(_translate("MainWindow", "BB"))
        self.baProbabilityLabel.setText(_translate("MainWindow", "BA"))
        self.useUserProbComboBox.setItemText(0, _translate("MainWindow", "Automatic"))
        self.useUserProbComboBox.setItemText(1, _translate("MainWindow", "Custom"))
        self.useUserProbLabel.setText(_translate("MainWindow", "Probability source"))
        self.automateComboBox.setItemText(0, _translate("MainWindow", "Manual"))
        self.automateComboBox.setItemText(1, _translate("MainWindow", "Automate"))
        self.automateLabel.setText(_translate("MainWindow", "Control Type"))
        self.taskTypeComboBox.setItemText(0, _translate("MainWindow", "Training"))
        self.taskTypeComboBox.setItemText(1, _translate("MainWindow", "ITS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_trainingWindow(MainWindow)
    ui.mainWindow.show()
    sys.exit(app.exec_())

