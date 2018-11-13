import sys
import numpy as np
import time
# from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtCore import QObject, QCoreApplication, QThread, pyqtSlot
# from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from dms_start_window import Ui_startWindow
from dms_training_window_mod import Ui_trainingWindow
from dms_model_nodaq import DMSModel
from its_model import ITSModel
import pyqtgraph as pg
import nidaqmx as ni
import nidaqmx.system, nidaqmx.stream_readers, nidaqmx.stream_writers
from nidaqmx.constants import LineGrouping
import thorlabs_apt as apt
from devices import Devices
skipStartUi = 1


class Controller(QObject):

    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        # self.startUi = Ui_startWindow()
        self.trainingUi = Ui_trainingWindow(QMainWindow())
        self.forward_moving_ports = True
        cd_ab = True
        self.devices = Devices(cd_ab=cd_ab, load_moving_ports=self.forward_moving_ports)
        dmsModel = DMSModel(cd_ab, self.devices, testing=False, moving_ports=self.forward_moving_ports)
        itsModel = ITSModel(cd_ab, self.devices, testing=False, moving_ports=self.forward_moving_ports, lr_moving_ports=True)
        if self.forward_moving_ports:
            self.devices.motors[1].move_to(self.devices.motors[1].position + 10)

        self.thread = QThread()
        dmsModel.moveToThread(self.thread)
        itsModel.moveToThread(self.thread)
        self.models = [dmsModel, itsModel]
        self.cur_model = 0

        self.showTrainingUi()

    #   START UI [not in use right now]
    def showStartUi(self):
        self.startUi.setupUi(self)
        self.startUi.goButton.clicked.connect(self.goButtonStartUi)
        self.startUi.dirButton.clicked.connect(self.chooseDirInStart)
        self.show()

    #   GO BUTTON FOR START UI [separate func necessary so user can type into line edits]
    def goButtonStartUi(self):
        programType = self.startUi.programLineEdit.text()
        if programType == 'training [default]' or programType == 'training' \
                or programType == 'Training':
            self.startUi.goButton.clicked.connect(self.showTrainingUi)

    #   TRAINING UI
    def showTrainingUi(self):
        """
        TRAINING UI
        """
        self.uiType = 'trainingUi'
        self.correct_avg = []
        self.bias = []

        #   AUTOFILLS
        self.trainingUi.curAnimalLineEdit.setText(self.models[self.cur_model].mouse)
        self.trainingUi.curPathLineEdit.setText(self.models[self.cur_model].save_path)

        self.timeLineEditBoxes = [self.trainingUi.itiLineEdit, self.trainingUi.noLickTimeLineEdit,
                                  self.trainingUi.odor1LineEdit, self.trainingUi.delay1LineEdit,
                                  self.trainingUi.odor2LineEdit, self.trainingUi.responseWindowLineEdit,
                                  self.trainingUi.consumptionTimeLineEdit]
        for i in range(len(self.timeLineEditBoxes)):
            self.timeLineEditBoxes[i].setText(str(self.models[self.cur_model].timing[i]))

        self.ubLineEdit = [self.trainingUi.aaUpperLineEdit, self.trainingUi.abUpperLineEdit,
                           self.trainingUi.bbUpperLineEdit, self.trainingUi.baUpperLineEdit]
        for i in range(len(self.ubLineEdit)):
            self.ubLineEdit[i].setText(str(int(self.models[self.cur_model].hi_bounds[i])))

        self.lbLineEdit = [self.trainingUi.aaLowerLineEdit, self.trainingUi.abLowerLineEdit,
                           self.trainingUi.bbLowerLineEdit, self.trainingUi.baLowerLineEdit]
        for i in range(len(self.lbLineEdit)):
            self.lbLineEdit[i].setText(str(int(self.models[self.cur_model].low_bounds[i])))

        self.trainingUi.minLicksLineEdit.setText(str(int(self.models[self.cur_model].min_licks)))
        self.trainingUi.ITSDelayDecrementLineEdit.setText("{:.3f}".format(self.models[1].delay_decrement))
        self.trainingUi.ITSDelayIncrementLineEdit.setText("{:.3f}".format(self.models[1].delay_increment))

        self.motorBoxes = [self.trainingUi.slowMotorSpeedLineEdit, self.trainingUi.slowMotorStepLineEdit,
                           self.trainingUi.fastMotorSpeedLineEdit, self.trainingUi.fastMotorStepLineEdit]

        slow_vel_param = self.devices.motors[0].get_velocity_parameters()
        self.motorBoxes[0].setText("{:.3f}".format(slow_vel_param[1]))
        self.motorBoxes[1].setText("{:.3f}".format(self.devices.sideways_motor_step))

        if self.forward_moving_ports:
            fast_vel_param = self.devices.motors[1].get_velocity_parameters()
            self.motorBoxes[2].setText("{:.3f}".format(fast_vel_param[1]))
            self.motorBoxes[3].setText("{:.3f}".format(self.devices.forward_motor_step))

        self.trainingUi.trialsToWaterLineEdit.setText("{}".format(self.models[self.cur_model].trials_to_water))

        #   BUTTON SIGNALS
        # self.trainingUi.backButton.clicked.connect(self.showStartUi)
        self.trainingUi.changePathButton.clicked.connect(self.changeDirTraining)
        self.trainingUi.startButton.clicked.connect(self.models[self.cur_model].run_program)
        self.trainingUi.stopButton.clicked.connect(self.stopProgram)
        # self.trainingUi.changeAnimalButton.clicked.connect(self.changeMouse)  # use lineEdit.returnPressed
        self.trainingUi.giveWaterButton.clicked.connect(self.giveWater)
        self.trainingUi.earlyLickCheckToggle.clicked[bool].connect(self.earlyLickToggle)

        #   DROPDOWN LISTS
        self.trainingUi.trialStructureComboBox.currentTextChanged.connect(self.changeTrialStruct)
        self.trainingUi.trialTypeComboBox.currentTextChanged.connect(self.changeTrialTypeMode)
        self.trainingUi.useUserProbComboBox.currentTextChanged.connect(self.changeProbSource)
        self.trainingUi.automateComboBox.currentTextChanged.connect(self.changeAutomate)
        self.trainingUi.taskTypeComboBox.currentTextChanged.connect(self.changeTaskType)
        self.trainingUi.movingPortComboBox.currentTextChanged.connect(self.changeMovingPorts)
        self.trainingUi.movingLRPortComboBox.currentTextChanged.connect(self.changeLRMovingPorts)

        #   models[self.cur_model] SIGNALS
        for i in range(2):
            self.models[i].startTrialSignal.connect(self.startTrialInputs)
            self.models[i].endTrialSignal.connect(self.endTrialInputs)
            self.models[i].intervalTime.connect(self.timeDisplay)
            self.models[i].lickSignal.connect(self.lickIndicator)
            self.models[i].refreshSignal.connect(self.clearPlots)

        self.timeBoxes = [self.trainingUi.itiTextBrowser, self.trainingUi.noLickTimeTextBrowser,
                          self.trainingUi.odor1TextBrowser, self.trainingUi.delay1TextBrowser,
                          self.trainingUi.odor2TextBrowser, self.trainingUi.responseWindowTextBrowser,
                          self.trainingUi.totalStimulusTextBrowser]

        self.waterBoxes = [self.trainingUi.leftWaterAmountLineEdit, self.trainingUi.rightWaterAmountLineEdit,
                           self.trainingUi.earlyLeftWaterAmountLineEdit, self.trainingUi.earlyRightWaterAmountLineEdit]

        self.itsDelayBoxes = [self.trainingUi.ITSDelayDecrementLineEdit, self.trainingUi.ITSDelayIncrementLineEdit]

        for i in range(len(self.waterBoxes)):
            self.waterBoxes[i].setText(str(float(self.models[self.cur_model].water_times[i])))

        for i in range(len(self.itsDelayBoxes)):
            self.itsDelayBoxes[i].setText("{:.3f}".format(self.models[1].delay_adjust[i]))

        #   USER INPUT CALLBACKS
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

        self.itsDelayBoxes[0].returnPressed.connect(lambda: self.itsDelayEditChanges(0))
        self.itsDelayBoxes[1].returnPressed.connect(lambda: self.itsDelayEditChanges(1))

        self.waterBoxes[0].returnPressed.connect(lambda: self.waterEditChanges(0))
        self.waterBoxes[1].returnPressed.connect(lambda: self.waterEditChanges(1))
        self.waterBoxes[2].returnPressed.connect(lambda: self.waterEditChanges(2))
        self.waterBoxes[3].returnPressed.connect(lambda: self.waterEditChanges(3))

        self.motorBoxes[0].returnPressed.connect(lambda: self.motorEditChanges(0))
        self.motorBoxes[1].returnPressed.connect(lambda: self.motorEditChanges(1))
        self.motorBoxes[2].returnPressed.connect(lambda: self.motorEditChanges(2))
        self.motorBoxes[3].returnPressed.connect(lambda: self.motorEditChanges(3))

        self.trainingUi.earlyLickCheckTimeLineEdit.returnPressed.connect(self.changeEarlyCheckTime)
        self.trainingUi.trialsToWaterLineEdit.returnPressed.connect(self.changeTrialsToWater)

        self.trainingUi.errorTOLineEdit.returnPressed.connect(lambda: self.changeErrorTO())
        self.trainingUi.errorTOLineEdit.setText("{}".format(self.models[self.cur_model].timeout[1]))
        self.trainingUi.earlyLickTOLineEdit.returnPressed.connect(lambda: self.changeEarlyTO())
        self.trainingUi.earlyLickTOLineEdit.setText("{}".format(self.models[self.cur_model].early_timeout))
        self.trainingUi.earlyLickCheckTimeLineEdit.setText("{}".format(self.models[self.cur_model].early_lick_time))

        self.trainingUi.minLicksLineEdit.returnPressed.connect(self.minLicksChanges)

        self.autoProbability = [self.trainingUi.aaProbabilityTextBrowser, self.trainingUi.abProbabilityTextBrowser,
                                self.trainingUi.bbProbabilityTextBrowser, self.trainingUi.baProbabilityTextBrowser]
        for i in range(len(self.autoProbability)):
            self.autoProbability[i].setText("{:.2f}".format(self.models[self.cur_model].probabilities[i]))

        self.customProbability = [self.trainingUi.aaProbabilityLineEdit, self.trainingUi.abProbabilityLineEdit,
                                  self.trainingUi.bbProbabilityLineEdit, self.trainingUi.baCustomProbabilityTextBrowser]
        for i in range(len(self.customProbability)):
            self.customProbability[i].setText("{:.2f}".format(self.models[self.cur_model].user_probabilities[i]))

        self.trainingUi.aaProbabilityLineEdit.returnPressed.connect(lambda: self.probEditChanges(0))
        self.trainingUi.abProbabilityLineEdit.returnPressed.connect(lambda: self.probEditChanges(1))
        self.trainingUi.bbProbabilityLineEdit.returnPressed.connect(lambda: self.probEditChanges(2))

        #   GRAPHICS
        self.led_color = QColor(110, 255, 130)
        self.led_off = QColor(0, 0, 0)

        self.pg_trialByTrial = self.trainingUi.trialByTrialGraphic
        self.pg_correctP = self.trainingUi.correctTrialsGraphic
        self.pg_bias = self.trainingUi.biasGraphic

        self.pg_trialByTrial.setMouseEnabled(x=True, y=False)
        self.pg_correctP.setMouseEnabled(x=True, y=False)
        self.pg_bias.setMouseEnabled(x=True, y=False)

        self.pg_trialByTrial.setYRange(0, 3, padding=None)
        self.pg_correctP.setYRange(0, 100, padding=None)

        self.trainingUi.leftLickIndicatorWidget.setStyleSheet(
            "QWidget { background-color: %s}" % self.led_off.name())
        self.trainingUi.rightLickIndicatorWidget.setStyleSheet(
            "QWidget { background-color: %s}" % self.led_off.name())

        self.changeTrialStruct()
        self.setDataTables()

        self.thread.start()
        self.trainingUi.mainWindow.show()

    def waterEditChanges(self, ix):
        try:
            self.models[self.cur_model].water_times[ix] = float(self.waterBoxes[ix].text())
            print(self.models[self.cur_model].water_times[ix])
        except:
            self.invalidInputMsg()

    def itsDelayEditChanges(self, ix):
        try:
            self.models[1].delay_adjust[ix] = float(self.itsDelayBoxes[ix].text())
        except:
            self.invalidInputMsg()

    def earlyLickToggle(self, pressed):
        if pressed:
            self.models[self.cur_model].early_lick_check = True
        else:
            self.models[self.cur_model].early_lick_check = False

    def changeEarlyCheckTime(self):
        try:
            t = float(self.trainingUi.earlyLickCheckTimeLineEdit.text())
            t = np.minimum(np.sum(self.models[self.cur_model].timing[2:5]), t)
            t = np.maximum(t, 0.)
            self.models[self.cur_model].early_lick_time = t
            self.trainingUi.earlyLickCheckTimeLineEdit.setText("{:.3f}".format(t))
        except:
            self.invalidInputMsg()

    def lickIndicator(self):
        ind = self.models[self.cur_model].indicator.flatten()
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
        self.models[self.cur_model].give_water = True

    def timeDisplay(self, t):
        self.timeBoxes[self.models[self.cur_model].cur_stage].setText("{:.3f}".format(t))
        if self.models[self.cur_model].cur_stage < 5:
            self.timeBoxes[-1].setText("{:.3f}".format(np.sum(self.models[self.cur_model].elapsed_time)))

    def changeTrialTypeMode(self):
        if self.cur_model == 1:  # ITS
            return
        trial_type = self.trainingUi.trialTypeComboBox.currentText()
        if trial_type == 'Full':
            self.models[self.cur_model].structure = 2
        elif trial_type == 'AA/AB':
            self.models[self.cur_model].structure = 0

    def changeTrialStruct(self):
        if self.cur_model == 1:  # ITS
            return
        trial_struct = self.trainingUi.trialStructureComboBox.currentText()
        self.trainingUi.trialStructTextBrowser.setText(trial_struct)
        self.models[self.cur_model].trial_type_progress *= 0
        if trial_struct == 'Random':
            self.models[self.cur_model].random = True
        elif trial_struct == 'Alternating':
            self.models[self.cur_model].random = False

    def changeMovingPorts(self):
        move_ports = self.trainingUi.movingPortComboBox.currentText()
        if move_ports == "Moving Ports":
            self.models[0].moving_ports = True
            self.models[1].moving_ports = True
            print("Forward moving ports on")
        else:
            self.models[0].moving_ports = False
            self.models[1].moving_ports = False
            print("Forward moving ports off")

    def changeLRMovingPorts(self):
        move_ports = self.trainingUi.movingLRPortComboBox.currentText()
        if move_ports == "Moving Ports":
            self.models[1].lr_moving_ports = True
            print("ITS left/right moving ports on")
        else:
            self.models[1].lr_moving_ports = False
            print("ITS left/right moving ports off")

    def changeProbSource(self):
        if self.cur_model == 1:  # ITS
            return
        source = self.trainingUi.useUserProbComboBox.currentText()
        if source == 'Automatic':
            self.models[self.cur_model].use_user_probs = False
        else:
            self.models[self.cur_model].use_user_probs = True

    def changeAutomate(self):
        if self.cur_model == 1:  # ITS
            return
        type = self.trainingUi.automateComboBox.currentText()
        if type == 'Manual':
            self.models[self.cur_model].automate = False
        else:
            self.models[self.cur_model].automate = True

    def changeTrialsToWater(self):
        try:
            self.models[self.cur_model].trials_to_water = float(self.trainingUi.trialsToWaterLineEdit.text())
        except:
            self.invalidInputMsg()

    def changeTaskType(self):  # mod
        cur_task = self.trainingUi.taskTypeComboBox.currentText()
        print(cur_task)
        if cur_task == 'Training':
            if self.cur_model == 0:  # no change
                return
            new_model = 0
            print('switched to DMS')

        elif cur_task == 'ITS':
            if self.cur_model == 1:  # no change
                return
            new_model = 1
            print('switched to ITS')

        else:
            return

        self.models[self.cur_model].run = False
        self.models[self.cur_model].refresh = True
        self.models[self.cur_model].refresh_metrics()
        self.clearPlots()

        # refresh save files and GUI button functions, transfer current save locations
        self.cur_model = new_model
        self.trainingUi.startButton.clicked.disconnect()
        self.trainingUi.startButton.clicked.connect(self.models[self.cur_model].run_program)
        for i in range(len(self.timeLineEditBoxes)):
            self.timeLineEditBoxes[i].setText(str(self.models[self.cur_model].timing[i]))
        print(self.models[self.cur_model].timing)

        for i in range(len(self.waterBoxes)):
            self.waterBoxes[i].setText(str(float(self.models[self.cur_model].water_times[i])))

        self.models[self.cur_model].early_lick_check = self.trainingUi.earlyLickCheckToggle.isChecked()
        self.models[self.cur_model].save_path = self.trainingUi.curPathLineEdit.text()
        self.trainingUi.earlyLickCheckTimeLineEdit.setText("{:.3f}".format(self.models[self.cur_model].early_lick_time))
        self.curAnimalChanges()
        # self.refreshSaveFiles()

    def startTrialInputs(self):
        print('Trial: {}'.format(self.models[self.cur_model].trial_num))
        self.trainingUi.trialNoTextBrowser.setText("{}".format(self.models[self.cur_model].trial_num))
        self.trainingUi.trialTypeTextBrowser.setText(['CA', 'CB', 'DB', 'DA'][self.models[self.cur_model].trial_type])
        for i in range(self.models[self.cur_model].num_trial_types):
            self.autoProbability[i].setText("{:.2f}".format(self.models[self.cur_model].probabilities[i]))

    def curAnimalChanges(self):
        if self.models[self.cur_model].mouse == self.trainingUi.curAnimalLineEdit.text():
            return  # erroneous quit here
        if self.models[self.cur_model].mouse:  # must come before models[self.cur_model].mouse is changed
            self.models[self.cur_model].refresh = True
            print("metric data has been refreshed due to mouse change")

        self.models[self.cur_model].mouse = self.trainingUi.curAnimalLineEdit.text()
        self.refreshSaveFiles()

    def timingEditChanges(self, idx):
        try:
            if self.cur_model == 1:  # ITS
                if idx == 2 or idx == 4:
                    self.timeLineEditBoxes[idx].setText('{:.3f}'.format(self.models[self.cur_model].timing[idx]))
                    return
            self.models[self.cur_model].timing[idx] = float(self.timeLineEditBoxes[idx].text())
        except:
            self.invalidInputMsg()

    def motorEditChanges(self, idx):
        try:
            if idx == 0:  # change slow velocity
                param = self.devices.motors[0].get_velocity_parameters()
                self.devices.motors[0].set_velocity_parameters(param[0], param[1], float(self.motorBoxes[0].text()))
            if idx == 1:  # change slow step size
                self.devices.sideways_motor_step = float(self.motorBoxes[1].text())
            elif idx == 2:  # change fast velocity
                param = self.devices.motors[1].get_velocity_parameters()
                self.devices.motors[1].set_velocity_parameters(param[0], param[1], float(self.motorBoxes[2].text()))
            elif idx == 3:  # change fast step size
                param = self.devices.motors[1].get_velocity_parameters()
                self.devices.forward_motor_step = float(self.motorBoxes[3].text())

            self.models[self.cur_model].timing[idx] = float(self.timeLineEditBoxes[idx].text())
        except:
            self.invalidInputMsg()

    def ubEditChanges(self, idx):
        try:
            self.models[self.cur_model].hi_bounds[idx] = int(self.ubLineEdit[idx].text())
        except:
            self.invalidInputMsg()

    def lbEditChanges(self, idx):
        try:
            self.models[self.cur_model].low_bounds[idx] = int(self.lbLineEdit[idx].text())
        except:
            self.invalidInputMsg()

    def minLicksChanges(self):
        try:
            self.models[self.cur_model].min_licks = int(self.trainingUi.minLicksLineEdit.text())
        except:
            self.invalidInputMsg()

    def changeErrorTO(self):
        try:
            self.models[self.cur_model].timeout[1:3] = int(self.trainingUi.errorTOLineEdit.text())
        except:
            self.invalidInputMsg()

    def changeEarlyTO(self):
        try:
            self.models[self.cur_model].early_timeout = int(self.trainingUi.earlyLickTOLineEdit.text())
        except:
            self.invalidInputMsg()

    def probEditChanges(self, idx):
        try:
            newsum = np.sum(self.models[self.cur_model].user_probabilities[:3]) - self.models[self.cur_model].user_probabilities[idx] \
                     + float(self.customProbability[idx].text())
            if newsum <= 1:
                self.models[self.cur_model].user_probabilities[idx] = float(self.customProbability[idx].text())
                self.models[self.cur_model].user_probabilities[3] = 1 - np.sum(self.models[self.cur_model].user_probabilities[:3])
                self.customProbability[3].setText("{:.2f}".format(self.models[self.cur_model].user_probabilities[3]))
            else:
                self.invalidInputMsg()
        except:
            self.invalidInputMsg()

    def endTrialInputs(self):
        self.plot()
        self.changeDataTables()
        if self.cur_model == 1:  # ITS
            ix = self.models[self.cur_model].delay_ix
            self.trainingUi.earlyLickCheckTimeLineEdit.setText("{:.3f}".format(self.models[self.cur_model].timing[ix]))

        print('trial has ended')

    def setDataTables(self):
        # define
        self.overall_table = self.trainingUi.overallPerformanceTableWidget
        self.trialType_table = self.trainingUi.trialTypePerformanceTableWidget

        # initiate table
        self.overall_table.setRowCount(self.models[self.cur_model].performance_overall.shape[0])
        self.overall_table.setColumnCount(self.models[self.cur_model].performance_overall.shape[1])
        self.overall_table.resize(140, 235)

        self.trialType_table.setRowCount(self.models[self.cur_model].performance_stimulus.shape[0])
        self.trialType_table.setColumnCount(self.models[self.cur_model].performance_stimulus.shape[1])
        self.trialType_table.resize(350, 125)

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
        overall_data = self.models[self.cur_model].performance_overall
        trialType_data = self.models[self.cur_model].performance_stimulus

        for i in range(overall_data.shape[0]):
            self.overall_table.setItem(i, 0, QTableWidgetItem(str(int(overall_data[i][0]))))  # trials
            self.overall_table.setItem(i, 1, QTableWidgetItem("{:.2f}".format(overall_data[i][1])))  # rate

        for i in range(trialType_data.shape[0]):
            for j in range(trialType_data.shape[1]):
                if j == 0:
                    self.trialType_table.setItem(i, j, QTableWidgetItem(str(int(trialType_data[i][j]))))
                else:
                    self.trialType_table.setItem(i, j, QTableWidgetItem("{:.2f}".format(trialType_data[i][j])))

    def plot(self):
        current_trial = self.models[self.cur_model].trial_num

        trial_num, trial_type, choice, early = self.models[self.cur_model].trialArray[-1]
        if choice == 0:  # correct
            symbolBrush = 'g'
        elif choice == 1:  # error
            symbolBrush = 'r'
        elif choice == 2:  # switch
            symbolBrush = 'y'
        else:  # miss
            symbolBrush = 'w'


        print(trial_num, trial_type, choice, early, symbolBrush)

        if early == 1:
            symbolPen = symbolBrush
            symbolBrush = None
        else:
            symbolPen = None

        # Trial-by-Trial Graphic
        self.pg_trialByTrial.plot([current_trial], [trial_type], pen=None, symbolBrush=symbolBrush, symbolPen=symbolPen)

        # set range of visible data
        if current_trial < 31:
            self.pg_trialByTrial.setXRange(0, 30, padding=None)
        else:
            self.pg_trialByTrial.setXRange(current_trial - 30, current_trial, padding=None)

        #   Correct Performance
        self.pg_correctP.plot(self.models[self.cur_model].correct_avg, pen='g', symbol=None, clear=True)
        if current_trial < 301:
            self.pg_correctP.setXRange(0, 300, padding=None)
        else:
            self.pg_correctP.setXRange(current_trial - 300, current_trial, padding=None)

        #   Bias
        self.pg_bias.plot(self.models[self.cur_model].bias, pen='w', symbol=None, clear=True)
        if current_trial < 101:
            self.pg_bias.setXRange(0, 100, padding=None)
        else:
            self.pg_bias.setXRange(current_trial - 100, current_trial, padding=None)

    def stopProgram(self):
        self.models[self.cur_model].run = False
        print("stopping...")
        # screenshot = QApplication.primaryScreen().grabWindow(0)
        # screenshot.save('scrnshot', 'png')
        # QApplication.clipboard().setImage(screenshot)

    def chooseDirInStart(self):
        self.chosendir = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.startUi.pathLineEdit.setText(self.chosendir)
        return self.chosendir

    def changeDirTraining(self):
        new_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        if new_dir == self.models[self.cur_model].save_path:
            return
        if self.models[self.cur_model].save_path:  # must come first
            self.models[self.cur_model].refresh = True
            print("metric data has been refreshed due to directory change")

        self.trainingUi.curPathLineEdit.setText(new_dir)
        self.models[self.cur_model].save_path = new_dir
        self.refreshSaveFiles()

    def refreshSaveFiles(self):
        self.models[self.cur_model].events_file = self.models[self.cur_model].save_path + '/' + self.models[self.cur_model].mouse + '_events'
        self.models[self.cur_model].licking_file = self.models[self.cur_model].save_path + '/' + self.models[self.cur_model].mouse + '_licking'
        self.clearPlots()

    def clearPlots(self):
        self.pg_trialByTrial.plot(clear=True)
        self.pg_correctP.plot(clear=True)
        self.pg_bias.plot(clear=True)

    def invalidInputMsg(self):
        msg = QErrorMessage()
        msg.showMessage("Invalid input")
        msg.exec()


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