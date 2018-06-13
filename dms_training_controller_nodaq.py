import sys
import numpy as np
import time as t
# from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtCore import QObject, QCoreApplication, QThread, pyqtSlot
# from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from dms_start_window import Ui_startWindow
from dms_training_window_mod import Ui_trainingWindow
from dms_model_nodaq import DMSModel as Model
import pyqtgraph as pg
skipStartUi = 1

#   INITIALIZE START UI
class Controller(QObject):

    def __init__(self):
        # super(controller, self).__init__(parent)
        super().__init__()
        # self.setupUi(self)
        # self.startUi = Ui_startWindow()
        self.trainingUi = Ui_trainingWindow(QMainWindow())
        self.model = Model()
        self.thread = QThread()
        self.model.moveToThread(self.thread)

        # if skipStartUi == 1:
        #     self.showTrainingUi()
        # else:
        #     self.showStartUi()

        self.showTrainingUi()

        # self.thread.started.connect(self.model.run_program)
        # self.model.endProgramSignal.connect(self.thread.quit)

    #   START UI [always the first window shown]
    def showStartUi(self):
        self.startUi.setupUi(self)
        self.startUi.goButton.clicked.connect(self.goButtonStartUi)
        self.startUi.dirButton.clicked.connect(self.chooseDirInStart)
        self.show()

    #   GO BUTTON FOR START UI [separate func necessary so user can type into line edits]
    def goButtonStartUi(self):
        programType = self.startUi.programLineEdit.text()
        if programType == 'training [default]' or programType == 'training'\
                or programType == 'Training':
            self.startUi.goButton.clicked.connect(self.showTrainingUi)

    #   TRAINING UI
    def showTrainingUi(self):
        self.correct_avg = []
        self.bias = []

        # Indicator colors
        self.led_color = QColor(110, 255, 130)
        self.led_off = QColor(0, 0, 0)

        # Autofills
        self.trainingUi.curAnimalLineEdit.setText(self.model.mouse)
        self.trainingUi.curPathLineEdit.setText(self.model.save_path)

        self.timeLineEditBoxes = [self.trainingUi.itiLineEdit, self.trainingUi.noLickTimeLineEdit,
                                  self.trainingUi.odor1LineEdit, self.trainingUi.delay1LineEdit,
                                  self.trainingUi.odor2LineEdit, self.trainingUi.responseWindowLineEdit,
                                  self.trainingUi.consumptionTimeLineEdit]
        for i in range(7):
            self.timeLineEditBoxes[i].setText(str(self.model.timing[i]))

        self.ubLineEdit = [self.trainingUi.aaUpperLineEdit, self.trainingUi.abUpperLineEdit,
                   self.trainingUi.bbUpperLineEdit, self.trainingUi.baUpperLineEdit]
        for i in range(4):
            self.ubLineEdit[i].setText(str(int(self.model.hi_bounds[i])))

        self.lbLineEdit = [self.trainingUi.aaLowerLineEdit, self.trainingUi.abLowerLineEdit,
                   self.trainingUi.bbLowerLineEdit, self.trainingUi.baLowerLineEdit]
        for i in range(4):
            self.lbLineEdit[i].setText(str(int(self.model.low_bounds[i])))

        self.trainingUi.minLicksLineEdit.setText(str(int(self.model.min_licks)))
        self.trainingUi.leftWaterAmountLineEdit.setText(str(float(self.model.water_times[0])))
        self.trainingUi.rightWaterAmountLineEdit.setText(str(float(self.model.water_times[1])))

        # BUTTON SIGNALS
        # self.trainingUi.backButton.clicked.connect(self.showStartUi)
        self.trainingUi.changePathButton.clicked.connect(self.changeDirTraining)
        self.trainingUi.startButton.clicked.connect(self.model.run_program)
        self.trainingUi.stopButton.clicked.connect(self.stopProgram)
        # self.trainingUi.changeAnimalButton.clicked.connect(self.changeMouse)  # use lineEdit.returnPressed
        self.trainingUi.giveWaterButton.clicked.connect(self.giveWater)

        # DROPDOWN LISTS
        self.trainingUi.trialStructureComboBox.currentTextChanged.connect(self.changeTrialStruct)
        self.trainingUi.trialTypeComboBox.currentTextChanged.connect(self.changeTrialTypeMode)
        self.trainingUi.useUserProbComboBox.currentTextChanged.connect(self.changeProbSource)

        # MODEL SIGNALS
        self.model.startTrialSignal.connect(self.startTrialInputs)
        self.model.endTrialSignal.connect(self.endTrialInputs)
        self.model.intervalTime.connect(self.timeDisplay)
        self.model.lickSignal.connect(self.lickIndicator)
        self.timeBoxes = [self.trainingUi.itiTextBrowser, self.trainingUi.noLickTimeTextBrowser,
                          self.trainingUi.odor1TextBrowser, self.trainingUi.delay1TextBrowser,
                          self.trainingUi.odor2TextBrowser, self.trainingUi.responseWindowTextBrowser,
                          self.trainingUi.totalStimulusTextBrowser]

        # USER INPUT CALLBACKS
        self.trainingUi.curAnimalLineEdit.returnPressed.connect(self.curAnimalChanges)

        self.timeLineEditBoxes[0].returnPressed.connect(lambda: self.timingEditChanges(0))
        self.timeLineEditBoxes[1].returnPressed.connect(lambda: self.timingEditChanges(1))
        self.timeLineEditBoxes[2].returnPressed.connect(lambda: self.timingEditChanges(2))
        self.timeLineEditBoxes[3].returnPressed.connect(lambda: self.timingEditChanges(3))
        self.timeLineEditBoxes[4].returnPressed.connect(lambda: self.timingEditChanges(4))
        self.timeLineEditBoxes[5].returnPressed.connect(lambda: self.timingEditChanges(5))
        self.timeLineEditBoxes[6].returnPressed.connect(lambda: self.timingEditChanges(6))

        self.trainingUi.aaUpperLineEdit.returnPressed.connect(lambda: self.ubEditChanges(0))
        self.trainingUi.abUpperLineEdit.returnPressed.connect(lambda: self.ubEditChanges(1))
        self.trainingUi.bbUpperLineEdit.returnPressed.connect(lambda: self.ubEditChanges(2))
        self.trainingUi.baUpperLineEdit.returnPressed.connect(lambda: self.ubEditChanges(3))

        self.trainingUi.aaLowerLineEdit.returnPressed.connect(lambda: self.lbEditChanges(0))
        self.trainingUi.abLowerLineEdit.returnPressed.connect(lambda: self.lbEditChanges(1))
        self.trainingUi.bbLowerLineEdit.returnPressed.connect(lambda: self.lbEditChanges(2))
        self.trainingUi.baLowerLineEdit.returnPressed.connect(lambda: self.lbEditChanges(3))

        self.trainingUi.errorTOLineEdit.returnPressed.connect(lambda: self.changeErrorTO())
        self.trainingUi.earlyLickTOLineEdit.returnPressed.connect(lambda: self.changeEarlyTO())

        self.trainingUi.minLicksLineEdit.returnPressed.connect(self.minLicksChanges)

        self.autoProbability = [self.trainingUi.aaProbabilityTextBrowser, self.trainingUi.abProbabilityTextBrowser,
                                self.trainingUi.bbProbabilityTextBrowser, self.trainingUi.baProbabilityTextBrowser]
        for i in range(4):
            self.autoProbability[i].setText("{:.2f}".format(self.model.probabilities[i]))

        self.customProbability = [self.trainingUi.aaProbabilityLineEdit, self.trainingUi.abProbabilityLineEdit,
                                  self.trainingUi.bbProbabilityLineEdit, self.trainingUi.baProbabilityLineEdit]
        self.trainingUi.aaProbabilityLineEdit.returnPressed.connect(lambda: self.probEditChanges(0))
        self.trainingUi.abProbabilityLineEdit.returnPressed.connect(lambda: self.probEditChanges(1))
        self.trainingUi.bbProbabilityLineEdit.returnPressed.connect(lambda: self.probEditChanges(2))
        self.trainingUi.baProbabilityLineEdit.returnPressed.connect(lambda: self.probEditChanges(3))

        self.changeTrialStruct()
        self.setDataTables()

        self.pg_trialByTrial = self.trainingUi.trialByTrialGraphic
        self.pg_correctP = self.trainingUi.correctTrialsGraphic
        self.pg_bias = self.trainingUi.biasGraphic

        self.pg_trialByTrial.setMouseEnabled(x=True, y=False)
        self.pg_correctP.setMouseEnabled(x=True, y=False)
        self.pg_bias.setMouseEnabled(x=True, y=False)

        self.pg_trialByTrial.setYRange(0, 3, padding=None)
        self.pg_correctP.setYRange(0, 100, padding=None)

        self.pg_trialByTrial.plot()

        # self.model.startTrialSignal.signal.connect(self.startTrialInputs)
        # self.model.endTrialSignal.signal.connect(self.endTrialInputs)

        self.thread.start()
        self.trainingUi.mainWindow.show() 

    def lickIndicator(self):
        ind = self.model.indicator.flatten()
        if ind[0]:
            self.trainingUi.leftLickIndicatorWidget.setStyleSheet(
                "QWidget { background-color: %s}" % self.led_color.name())
        else:
            self.trainingUi.leftLickIndicatorWidget.setStyleSheet(
                "QWidget { background-color: %s}" % self.led_off.name())

        if ind[1]:
            self.trainingUi.rightLickIndicatorWidget.setStyleSheet(
                "QWidget { background-color: %s}" % self.led_color.name())
        else:
            self.trainingUi.rightLickIndicatorWidget.setStyleSheet(
                "QWidget { background-color: %s}" % self.led_off.name())

    def giveWater(self):
        self.model.give_water = True

    def timeDisplay(self, t):
        self.timeBoxes[self.model.cur_stage].setText("{:.3f}".format(t))
        if self.model.cur_stage < 5:
            self.timeBoxes[-1].setText("{:.3f}".format(np.sum(self.model.total_time)))

    def changeTrialTypeMode(self):
        trial_type = self.trainingUi.trialTypeComboBox.currentText()
        # self.trainingUi.trialTypeTextBrowser.setText(self.curTrialTypeMode)
        if trial_type == 'Full':
            self.model.structure = 2
        elif trial_type == 'AA/AB':
            self.model.structure = 0

    def changeTrialStruct(self):
        trial_struct = self.trainingUi.trialStructureComboBox.currentText()
        self.trainingUi.trialStructTextBrowser.setText(trial_struct)  # this is redundant
        self.model.trial_type_progress *= 0
        if trial_struct == 'Random':
            self.model.random = True
        elif trial_struct == 'Alternating':
            self.model.random = False

    def changeProbSource(self):
        source = self.trainingUi.useUserProbComboBox.currentText()
        if source == 'Automatic':
            self.model.use_user_probs = False
        else:
            self.model.use_user_probs = True

    def startTrialInputs(self, i):
        print('Trial: {}'.format(i))
        self.trainingUi.trialNoTextBrowser.setText("{}".format(i))
        self.trainingUi.trialTypeTextBrowser.setText(['AA', 'AB', 'BB', 'BA'][self.model.trial_type])

        # self.trainingUi.itiLineEdit.returnPressed.connect(lambda: self.lineEditChanges('iti'))
        # self.trainingUi.noLickTimeLineEdit.returnPressed.connect(lambda: self.lineEditChanges('noLick'))
        # self.trainingUi.odor1LineEdit.returnPressed.connect(lambda: self.lineEditChanges('odor1'))
        # self.trainingUi.delay1LineEdit.returnPressed.connect(lambda: self.lineEditChanges('delay'))
        # self.trainingUi.odor2LineEdit.returnPressed.connect(lambda: self.lineEditChanges('odor2'))
        # self.trainingUi.responseWindowLineEdit.returnPressed.connect(lambda: self.lineEditChanges('response'))

    def curAnimalChanges(self):
        if self.model.mouse:  # must come before model.mouse is changed
            self.model.refresh = True
            print("metric data has been refreshed due to mouse change")

        self.model.mouse = self.trainingUi.curAnimalLineEdit.text()
        self.refreshSaveFiles()

    def timingEditChanges(self, idx):
        try:
            self.model.timing[idx] = float(self.timeLineEditBoxes[idx].text())
        except:
            self.invalidInputMsg()

    def ubEditChanges(self, idx):
        try:
            self.model.hi_bounds[idx] = int(self.ubLineEdit[idx].text())
        except:
            self.invalidInputMsg()

    def lbEditChanges(self, idx):
        try:
            self.model.low_bounds[idx] = int(self.lbLineEdit[idx].text())
        except:
            self.invalidInputMsg()

    def minLicksChanges(self):
        try:
            self.model.min_licks = int(self.trainingUi.minLicksLineEdit.text())
        except:
            self.invalidInputMsg()

    def probEditChanges(self, idx):
        try:
            self.model.user_probabilities[idx] = int(self.customProbability[idx].text())
        except:
            self.invalidInputMsg()

    def endTrialInputs(self):
        self.plot()
        self.changeDataTables()
        # n=300
        # self.trainingUi.trialNoTextBrowser.setText(str(self.model.trial_num))
        # pos = np.random.normal(size=(2, n), scale=1e-5)
        # spots = [{'pos': pos[:, i], 'data': 1} for i in range(n)] + [{'pos': [0, 0], 'data': 1}]
        # self.trainingUi.trialByTrialGraphic.addPoints(spots)
        # self.trainingUi.trialNoTextBrowser.setText(str(self.model.trial_num))
        print('trial has ended')

    def setDataTables(self):
        # define
        self.overall_table = self.trainingUi.overallPerformanceTableWidget
        self.trialType_table = self.trainingUi.trialTypePerformanceTableWidget

        # initiate table
        self.overall_table.setRowCount(self.model.performance_overall.shape[0])
        self.overall_table.setColumnCount(self.model.performance_overall.shape[1])
        self.overall_table.resize(140,235)

        self.trialType_table.setRowCount(self.model.performance_stimulus.shape[0])
        self.trialType_table.setColumnCount(self.model.performance_stimulus.shape[1])
        self.trialType_table.resize(245, 117)

        # set labels
        self.overall_table.setHorizontalHeaderLabels(['trials', 'rate   '])
        self.overall_table.setVerticalHeaderLabels(['correct', 'error', 'switch', 'miss', 'early_lick',
                                                    'left', 'right', 'l_reward', 'r_reward'])
        self.overall_table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.overall_table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.overall_table.resizeColumnsToContents()
        self.overall_table.resizeRowsToContents()

        self.trialType_table.setVerticalHeaderLabels(['AA', 'AB', 'BB', 'BA'])
        self.trialType_table.setHorizontalHeaderLabels(['trials ', '% perfect', 'correct', 'error  ', 'switch ',
                                                        'miss', 'early'])
        self.trialType_table.resizeColumnsToContents()
        self.trialType_table.resizeRowsToContents()

    def changeDataTables(self):
        overall_data = self.model.performance_overall
        trialType_data = self.model.performance_stimulus

        for i in range(overall_data.shape[0]):
            self.overall_table.setItem(i, 0, QTableWidgetItem(str(int(overall_data[i][0]))))  # trials
            self.overall_table.setItem(i, 1, QTableWidgetItem(str(overall_data[i][1])))  # rate

        for i in range(trialType_data.shape[0]):
            for j in range(trialType_data.shape[1]):
                self.trialType_table.setItem(i, j, QTableWidgetItem(str(int(trialType_data[i][j]))))

    def plot(self):
        current_trial = self.model.trial_num

        #   Trial-by-Trial Graphic
        self.pg_trialByTrial.plot(self.model.correct_trials[0], self.model.correct_trials[1], pen=None, symbol='o', symbolBrush='g')
        self.pg_trialByTrial.plot(self.model.error_trials[0], self.model.error_trials[1], pen=None, symbol='o', symbolBrush='r')
        self.pg_trialByTrial.plot(self.model.switch_trials[0], self.model.switch_trials[1], pen=None, symbol='o', symbolBrush='y')
        self.pg_trialByTrial.plot(self.model.miss_trials[0], self.model.miss_trials[1], pen=None, symbol='o', symbolBrush='w')
        if current_trial < 31:  # set range of visible data
            self.pg_trialByTrial.setXRange(0, 30, padding=None)
        else:
            self.pg_trialByTrial.setXRange(current_trial-30, current_trial, padding=None)

        #   Correct Performance
        self.pg_correctP.plot(self.model.correct_avg, pen='g', symbol=None)
        if current_trial < 301:
            self.pg_correctP.setXRange(0,300,padding=None)
        else:
            self.pg_correctP.setXRange(current_trial-300, current_trial, padding=None)

        #   Bias
        self.pg_bias.plot(self.model.bias, pen='w', symbol=None)
        if current_trial < 101:
            self.pg_bias.setXRange(0,100,padding=None)
        else:
            self.pg_bias.setXRange(current_trial-100, current_trial, padding=None)

    def stopProgram(self):
        self.model.run = False
        print("stopping...")
        # screenshot = QApplication.primaryScreen().grabWindow(0)
        # screenshot.save('scrnshot', 'png')
        # QApplication.clipboard().setImage(screenshot)

    def chooseDirInStart(self):
        self.chosendir = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.startUi.pathLineEdit.setText(self.chosendir)
        return self.chosendir

    def changeDirTraining(self):
        if self.model.save_path:  # must come first
            self.model.refresh = True
            print("metric data has been refreshed due to directory change")
        new_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.trainingUi.curPathLineEdit.setText(new_dir)
        self.model.save_path = new_dir
        self.refreshSaveFiles()
        # self.model.refresh = True

    def changeErrorTO(self):
        try:
            self.model.timeout[1:3] = int(self.trainingUi.errorTOLineEdit.text())
        except:
            self.invalidInputMsg()

    def changeEarlyTO(self):
        try:
            self.model.early_timeout = int(self.trainingUi.earlyLickTOLineEdit.text())
        except:
            self.invalidInputMsg()

    def refreshSaveFiles(self):
        self.model.events_file = self.model.save_path + '/' + self.model.mouse + '_events'
        self.model.licking_file = self.model.save_path + '/' + self.model.mouse + '_licking'

    def invalidInputMsg(self):
        msg = QErrorMessage()
        msg.showMessage("Invalid input")
        msg.exec()

"""
TO-DO:
- stop program button
- controls
- indicator numbers
- indicator graphs
"""

# Code to stop 'python has stopped working' error
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Controller()

    # sys.exit(app.exec_())

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")