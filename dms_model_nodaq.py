import time, random
import numpy as np
import pandas as pd
import nidaqmx as ni
import nidaqmx.system, nidaqmx.stream_readers, nidaqmx.stream_writers
from nidaqmx.constants import LineGrouping
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
import sys, os, csv, collections
import thorlabs_apt as apt
from devices import Devices

np.random.seed(2)
EPS = np.finfo(float).eps

class DMSModel(QObject):
    """
    Model for the DMS training program. Will be adjusted to abstract
    repeated functions when moving to other programs.
    """

#   Signals
    lickSignal = pyqtSignal()
    startTrialSignal = pyqtSignal()
    endTrialSignal = pyqtSignal()
    refreshSignal = pyqtSignal()
    intReady = pyqtSignal(int)
    intervalTime = pyqtSignal(float)

    def __init__(self, devices, testing=False, moving_ports=True):
        super().__init__()
        self.num_trial_types = 4
        self.testing = testing
        self.moving_ports = moving_ports

        # performance
        self.trial_num = 0
        self.trial_type_history = []
        self.trial_correct_history = []
        self.trialArray = []  # make a single list of (trial number, choice, early)
        self.indicator = np.array([[False], [False]])
        self.prev_indicator = np.array([[False], [False]])
        self.performance_overall = np.zeros((9, 2))  # was 8 2
        # correct, error, switch, miss, early_lick, left, right, l reward, r reward
        # left column numbers, right column 
        self.performance_stimulus = np.zeros((self.num_trial_types, 7))
        # num trials, % perfect, %correct, %error, %switch, %miss, %early
        self.licking_export = []
        # trial no, tr_type, perfect, correct, error, switch, miss, early_lick,
        # left, right, L_rew, R_rew, iti_st, tr_st, stim_st, 1st_odor, delay,
        # 2nd_odor, 2nd_delay, go_tone, effective lick, L rew time, R rew time,
        # noise_onset, tr_end
        self.correct_avg = []
        self.bias = []

        # Trial selection
        self.trial_type = 0  # current trial type
        self.random_hi_bound = -1  # starting value
        self.low_bounds = np.ones(self.num_trial_types)
        self.hi_bounds = np.ones(self.num_trial_types) * 3
        self.structure = 2  # 0 for AA/AB, 1 for BB/BA, 2 for Full
        self.trial_type_progress = np.zeros(2)  # correct count, total number of trial type seen
        self.probabilities = np.ones(self.num_trial_types) / self.num_trial_types
        self.prev_trial = np.zeros(3)
        self.strict_ub = 10  # number of trials before the program switches trials automatically
        self.correct_choice = 0
        self.min_trial_to_auto = np.array([30, 30])  # number of trials to check before auto change. 0 alt, 1 random

        # User options
        self.random = False
        self.automate = False
        self.use_user_probs = False
        self.user_probabilities = self.probabilities.copy()
        self.save_path = ''  # save location
        self.mouse = 'test'  # Mouse name
        self.events_file = ''
        self.licking_file = ''
        self.run = False
        self.refresh = False

        # Timing - values in seconds
        self.min_licks = 2
        self.cur_stage = 0
        self.elapsed_time = np.zeros(4)  # odor1, delay, odor2, response
        # iti, no lick, odor1, delay, odor2, response, consumption
        if self.testing:
            # self.timing = [.1] * 7  # for testing
            self.timing = [1, .4, .5, 1.5, .5, 3, 1]  # standard times
            self.early_timeout = 1.0
            self.timeout = np.array([0.0, 1., 1., 0.])  # timeout for correct, error, switch, miss
        else:
            self.timing = [3, .4, .5, 1.5, .5, 3, 1]  # standard times
            self.early_timeout = 6.0
            self.timeout = np.array([0.0, 5., 5., 0.])  # timeout for correct, error, switch, miss

        self.early_lick_check = False
        self.early_lick_time = 0.0

        # water output
        self.trials_to_water = 5
        self.water_times = [.06, .06, .03, .03]
        self.give_water = False
        # DAQ output arrays
        self.all_low = [False] * 8
        self.go_cue = [False] * 8
        self.light = [False] * 8
        self.siren = [False] * 8

        self.go_cue[2] = True
        self.light[3] = True
        self.siren[4] = True

        odor_a = list(self.all_low)  # list() can be used to make a copy
        odor_a[5] = True
        odor_a[7] = True

        odor_b = list(self.all_low)
        odor_b[6] = True
        odor_b[7] = True

        odor_c = list(self.all_low)
        odor_c[0] = True

        odor_d = list(self.all_low)
        odor_d[1] = True

        self.blank = list(self.all_low)
        self.blank[7] = True

        self.trial_dict = {0: [odor_c, odor_a],
                           1: [odor_c, odor_b],
                           2: [odor_d, odor_a],
                           3: [odor_d, odor_b]}

        lw = list(self.all_low)
        lw[0] = True
        rw = list(self.all_low)
        rw[1] = True

        self.water_daq = [lw, rw]
        self.output = [False] * 8
        time.perf_counter()

        self.lickSideCounter = [0]*2
        self.motors = devices.motors
        self.out_tasks = devices.out_tasks
        self.in_task = devices.in_task
        self.reader = devices.reader
        self.devices = devices

    def update_indicator(self):
        self.prev_indicator = self.indicator.copy()
        if not self.testing:
            self.reader.read_one_sample_multi_line(self.indicator)

        if not np.array_equal(self.indicator, self.prev_indicator):
            self.lickSignal.emit()
            time.sleep(.001)
            self.licking_export.append([time.perf_counter(), int(self.indicator[0]), int(self.indicator[1])])

    def choose_alternating_trial(self):
        """
        Choose the next alternating trial type to run. A number of correct trials is
        selected from the bounds input by the user.
        """
        # if first trial, create a starting hi bound
        # upper bound is a random integer from lb to ub
        if self.random_hi_bound == -1:
            self.set_trial_hi()

        # check if num correct is >= hi bound
        if self.trial_type_progress[0] >= self.random_hi_bound \
                or self.trial_type_progress[1] >= self.strict_ub:
            if self.structure == 0:  # AA/AB
                self.trial_type = (self.trial_type + 1) % 2
            elif self.structure == 1:  # BB/BA
                self.trial_type = 2 + ((self.trial_type + 1) % 2)
            else:  # Full
                self.trial_type = (self.trial_type + 1) % 4

            self.trial_type_progress *= 0
            self.set_trial_hi()

        if self.automate:
            trange = self.min_trial_to_auto[0]
            if self.trial_num >= trange:
                trials_in_range = self.trial_correct_history[(len(self.trial_correct_history)-trange)
                                                             :len(self.trial_correct_history)]
                recent_avg = collections.Counter(trials_in_range)[0] / trange
                if recent_avg >= .8:
                    self.random = True

    def choose_random_trial(self):
        """
        Choose the next random trial to run. A trial type is selected and set to run
        for a random number of times, regardless of the number correct.
        """
        if self.random_hi_bound == -1:
            self.set_trial_hi()

        # check if total num seen is >= hi bound
        if self.trial_type_progress[1] >= self.random_hi_bound:
            if self.structure == 0:  # AA/AB
                self.trial_type = (self.trial_type + 1) % 2
            elif self.structure == 1:  # BB/BA
                self.trial_type = 2 + ((self.trial_type + 1) % 2)
            else:  # Full - sample a trial type
                self.trial_type = self.trial_sample()

            self.trial_type_progress *= 0
            self.set_trial_hi()

        if self.automate:
            trange = self.min_trial_to_auto[1]
            if self.trial_num >= trange:
                trials_in_range = self.trial_correct_history[(len(self.trial_correct_history) - trange)
                                                             :len(self.trial_correct_history)]
                recent_avg = collections.Counter(trials_in_range)[0] / trange
                if recent_avg <= .8:
                    self.random = False

    def set_trial_hi(self):
        """Make the above code less wordy with this shortcut."""
        self.random_hi_bound = np.random.randint(self.low_bounds[self.trial_type],
                                                 self.hi_bounds[self.trial_type] + 1)

    def trial_sample(self):
        """Sample a trial type from the full set of trials, minus the current trial type."""
        # create a cumulative distribution function
        if self.use_user_probs:
            tmp = np.exp(self.probabilties)
        else:
            tmp = np.exp(self.user_probabilities)

        cdf = tmp / (np.sum(tmp) - tmp[self.trial_type])
        cdf[self.trial_type] = 0
        for i in range(1, cdf.shape[0]):
            cdf[i] += cdf[i-1]

        # sample from the cdf
        p = np.random.rand()
        trial_type = 0
        while p > cdf[trial_type]:
            trial_type += 1

        return trial_type

    def run_interval(self, delay):
        """A generic delay between stages of the task."""
        st = time.time()
        t = 0
        if self.cur_stage == 0:
            self.output = self.light
            self.write(0)

        while t < delay:
            time.sleep(.001)
            t = time.time() - st
            self.update_indicator()
            if self.cur_stage == 3:
                # stimulus time is staggered by two indices - only delay uses this function during stimulus
                self.elapsed_time[self.cur_stage - 2] = t

            if self.cur_stage < 5:
                self.intervalTime.emit(t)

        if self.cur_stage == 0:
            self.output = self.all_low
            self.write(0)

    def run_no_lick(self):
        """Delay the trial until the mouse stops licking for a desired time."""
        no_lick = False
        st = time.time()
        while not no_lick:
            """
            1. check for lick
            2. if lick, restart time
            3. if no lick, check time passed
            """
            time.sleep(.001)
            self.update_indicator()
            if np.sum(self.indicator) > 0:
                st = time.time()

            t = time.time() - st
            self.intervalTime.emit(t)
            # if t > self.no_lick:
            if t > self.timing[1]:  # no lick time stage 1
                no_lick = True

    def run_odor(self, cue):
        """
        Release odors.
        :param cue: 0 or 1, denoting the odor delivery stage.
        """
        st = time.time()
        t = 0
        # while t < self.odor_times[cue]:
        early = 0
        self.output = list(self.trial_dict[self.trial_type][cue])
        self.write(1-cue)  # cue 0 means odors on daq 1, cue 1 means odors on daq 0

        while t < self.timing[2 + cue*2]:
            # cue is 0 (first odor) or 1 (second odor); odor stages are 2 or 4
            time.sleep(.001)
            t = time.time() - st
            # stimulus time is staggered by two indices
            self.elapsed_time[self.cur_stage - 2] = t
            self.intervalTime.emit(t)
            self.update_indicator()

            if cue == 1 and self.early_lick_check:  # second odor
                if np.sum(self.indicator) > 0 and t < self.early_lick_time:
                    early = 1

        if self.testing:
            pass
            # early = np.random.randint(2)

        self.output = list(self.all_low)
        self.write(0)
        self.write(1)
        return early

    def run_blank(self):
        # punishment blank
        st = time.time()
        t = 0
        self.output = list(self.blank)
        self.write(0)
        while t < .15:
            time.sleep(.001)
            t = time.time() - st
            self.intervalTime.emit(t)
            self.update_indicator()

        self.output = list(self.all_low)
        self.write(0)

    def write(self, daq):  # a cleaner function to call
        # self.writer.write_one_sample_multi_line(self.output)
        if not self.testing:
            self.out_tasks[daq].write(self.output)

    def determine_choice(self):
        """
        Determine whether the mouse has chosen left or right.
        outputs -
        choice: the decision made by the mouse. 0 is correct, 1 is error, 2 is a switch, 3 is a miss.
        result: a list with length 4 for correct/error/switch/miss. One-hot for the index given by choice.
            For performance updates.
        side: the side chosen by the mouse. -1 for a switch or miss, 0 left, 1 right.
        """
        st = time.time()
        t = 0
        licks = np.zeros((2, 1))
        active = False
        choice = 3  # miss
        result = [0] * 4
        side = -1
        # choice = 0 - correct, 1 - error, 2 - switch, 3 - miss
        self.output = self.go_cue
        self.write(0)
        while t < .15:
            time.sleep(.001)
            t = time.time() - st
            self.update_indicator()

        self.output = self.all_low
        self.write(0)

        t = 0
        # while t <= self.response_window:
        while t <= self.timing[self.cur_stage]:
            time.sleep(.001)
            t = time.time() - st
            self.elapsed_time[self.cur_stage - 2] = t
            self.intervalTime.emit(t)

            self.update_indicator()
            sum_ind = np.sum(self.indicator)
            if np.sum(sum_ind > 1):
                # error, licked both at the same time
                self.performance_overall[1, self.correct_choice] += 1
                choice = 1
                break  # continue?

            # check if starting a new lick
            if not active and sum_ind == 1:
                active = True
                licks += self.indicator

            # reset active once a lick is complete
            if active and sum_ind == 0:
                active = False

            # check for a switch
            if np.sum(licks > 0) == 2:
                choice = 2
                break

            # check for a choice
            if np.sum(licks) == 2:
                side = np.argmax(licks)
                if side == self.correct_choice:
                    choice = 0  # correct
                    self.give_water = True
                else:
                    choice = 1  # error
                break

            # Testing
            if self.testing:
                choice = np.random.randint(0, 2)
                if choice == 0:
                    side = self.correct_choice
                    self.give_water = True
                else:
                    side = 1 - self.correct_choice
                    self.give_water = False
                break
                # side = random.getrandbits(1)
                # if side == self.correct_choice:
                #     choice = 0  # correct
                #     self.give_water = True
                # else:
                #     choice = 1  # error
                #     self.give_water = False
                # break

        self.trial_correct_history.append(choice)
        result[choice] = 1
        return choice, result, side

    def deliver_water(self, early, side):
        """Deliver water, assuming the right choice was made."""
        st = time.time()
        early *= self.early_lick_check  # no water penalty if lick check is off
        water_time = self.water_times[self.correct_choice + early*2]
        self.output = list(self.water_daq[self.correct_choice])
        self.write(0)
        while (time.time() - st) < water_time:
            self.update_indicator()
            self.output = list(self.water_daq[side])

        print('water delivered')
        self.output = list(self.all_low)
        self.write(0)
        # self.out_task.write()

    def shut_down(self):
        self.out_tasks[0].stop()
        self.out_tasks[1].stop()
        self.in_task.stop()
        self.out_tasks[0].close()
        self.out_tasks[1].close()
        self.in_task.close()

    def save(self, event):
        with open(self.events_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(event)

        with open(self.licking_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.licking_export)

    def refresh_metrics(self):
        """Refresh performance metrics for when a new mouse or new directory is chosen."""
        # performance
        self.trial_num = 0
        self.trial_type_history = []
        self.trial_correct_history = []
        self.trialArray = []
        self.correct_avg = []
        self.performance_overall *= 0
        self.performance_stimulus *= 0
        self.licking_export = []
        self.trial_type = 0  # current trial type
        self.trial_type_progress *= 0  # correct count, total number of trial type seen
        self.prev_trial *= 0
        self.correct_avg = []
        self.bias = []
        self.correct_trials = [[], []]
        self.error_trials = [[], []]
        self.switch_trials = [[], []]
        self.miss_trials = [[], []]
        self.probabilities = np.ones(self.num_trial_types) / self.num_trial_types

    def update_probabilities(self):
        perc_corr = self.performance_stimulus[:,2] / (self.performance_stimulus[:,0] + np.finfo(float).eps)
        avg_perc_correct = np.mean(perc_corr)
        diff = perc_corr - avg_perc_correct
        diff *= 2 / self.num_trial_types
        p = np.ones(self.num_trial_types) / self.num_trial_types - diff
        if np.sum(np.isnan(p)) > 0:
            return
        else:
            self.probabilities = self.softmax(p)
            print("Probabilities: ", self.probabilities)

    def prepare_plot_data(self, choice, early):
        self.trialArray.append((self.trial_num, self.trial_type, choice, early))
        if self.trial_num < 30:
            tmp = self.trial_correct_history
        else:
            tmp = self.trial_correct_history[-30:]
        # self.correct_avg.append(np.sum(tmp[tmp == 0]) / len(tmp) * 100)
        self.correct_avg.append(collections.Counter(tmp)[0] / (len(tmp) + np.finfo(float).eps) * 100)

        self.bias.append(self.performance_overall[5,0] - self.performance_overall[6,0])

    def update_performance(self, choice, result, early, lick):
        """
        Update the metrics for peformance by stimulus and overall performance.
        :param choice: From determine_choice, the lick decision of the mouse (0->3).
        :param result: From determine_choice, and a
        :param early: early lick - 0 for no, 1 for yes
        :param lick: [left licked, right licked, left correct, right correct] for overall performance
        :return:
        """
        print(choice, result, early, lick)
        # performance_stimulus
        # num trials, % perfect, %correct, %error, %switch, %miss, %early
        # get total number of a result, add 1 and divide by new total trial type
        # multiply % of each result by total num
        cnt = self.performance_stimulus[self.trial_type, 1:] * self.performance_stimulus[self.trial_type, 0]
        self.performance_stimulus[self.trial_type, 0] += 1
        if choice == 0:
            if early == 0:  # perfect
                cnt[0] += 1
            else:
                cnt[-1] += 1

        cnt[1 + choice] += 1
        self.performance_stimulus[self.trial_type, 1:] = cnt / (self.performance_stimulus[self.trial_type, 0] + EPS)

        # performance_overall
        # correct, error, switch, miss, early_lick, left, right, l reward, r reward
        # left column numbers, right column percent
        self.performance_overall[:, 0] += np.array(result + [early] + lick)
        self.performance_overall[:, 1] = self.performance_overall[:, 0] / (self.trial_num + EPS)

    @staticmethod
    def softmax(x):
        """
        Compute softmax vector of x.
        :param x: input vector of log probabilities.
        :return: y, softmax vector
        """
        x = np.exp(x - np.amax(x))  # normalization to max of 0
        return x / np.sum(x)

    @pyqtSlot()
    def run_program(self):
        """Run the training program until the controller stops it."""
        # set the next trial
        # if self.automate:
            # check the percent correct

        self.run = True
        self.refresh = False
        choice = 0
        early = 0
        trials_to_water_counter = 0
        while self.run:
            # File I/O
            if not self.testing:
                if self.events_file == '':
                    print("You must specify a save folder.")
                    return

                if not os.path.isfile(self.events_file):
                    with open(self.events_file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['trial_no.', 'trial_type', 'perfect', 'correct', 'error', 'switch',
                                         'miss', 'early_lick', 'left', 'right', 'L_reward', 'R_reward', 'ITI_start',
                                         'trial_start', 'stimulus_start', '1st_odor_onset', 'delay_onset',
                                         '2nd_odor_onset', '2nd_delay_onset', 'Go_tone', 'effective_lick',
                                         'L_reward', 'R_reward', 'noise_onset', 'trial_end'])

                    with open(self.licking_file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['timestamp', 'left', 'right'])

            time.sleep(.001)  # need sleep time for graph
            self.elapsed_time *= 0
            if self.random:
                self.choose_random_trial()
            else:
                self.choose_alternating_trial()

            self.correct_choice = self.trial_type % 2
            self.trial_type_history.append(self.trial_type)
            self.trial_type_progress[1] += 1
            self.trial_num += 1
            self.startTrialSignal.emit()

            events = [self.trial_num, self.trial_type]
            times = ['NaN'] * 13

            # trial structure
            # print('iti')
            self.cur_stage = 0
            t_idx = 0
            times[t_idx] = time.perf_counter()  # iti start
            t_idx += 1
            iti = self.timing[self.cur_stage] + self.timeout[choice] +\
                  self.early_timeout * early * int(self.early_lick_check)
            self.run_interval(iti)

            # print('no lick')
            self.cur_stage += 1  # 1
            times[t_idx] = time.perf_counter()  # trial start
            t_idx += 1
            self.run_no_lick()

            # print('odor1')
            self.cur_stage += 1  # 2
            times[t_idx:t_idx+2] = [time.perf_counter()] * 2
            t_idx += 2  # stimulus and odor 1 start
            self.run_odor(0)

            # print('delay')
            self.cur_stage += 1  # 3
            times[t_idx] = time.perf_counter()  # delay start
            t_idx += 1
            # self.run_interval(self.delay)
            self.run_interval(self.timing[self.cur_stage])

            # print('odor2')
            self.cur_stage += 1  # 4
            times[t_idx] = time.perf_counter()  # odor 2 start
            t_idx += 1
            early = self.run_odor(1)
            t_idx += 1

            # print('response')
            # lick detection/response window
            self.cur_stage += 1  # 5
            # move lick ports to mouse
            if self.moving_ports:
                self.devices.move_forward()

            times[t_idx] = time.perf_counter()  # go tone
            t_idx += 1
            choice, result, side = self.determine_choice()
            if choice != 3:  # effective lick
                times[t_idx] = time.perf_counter()

            t_idx += 1
            perfect = np.maximum(result[0] - early, 0)
            lick = [0] * 4  # [left licked, right licked, left correct, right correct]
            if side != -1:
                lick[side] = 1
                self.lickSideCounter[side] += 1

            if self.give_water:  # aka choice = 1
                self.trial_type_progress[0] += 1
                lick[2 + self.correct_choice] = 1
                times[t_idx + self.correct_choice] = time.perf_counter()  # L/R reward
                trials_to_water_counter = 0
            elif trials_to_water_counter >= self.trials_to_water:
                trials_to_water_counter = 0
                self.deliver_water(early)
            else:
                # increase trials-to-water counter
                trials_to_water_counter += 1

            if choice == 1 or choice == 2:  # error, switch
                self.run_blank()

            t_idx += 2
            self.give_water = False
            self.update_performance(choice, result, early, lick)
            self.prepare_plot_data(choice, early)

            # consumption time
            self.run_interval(self.timing[-1])  # consumption time is last
            # remove ports from mouse
            if self.moving_ports:
                self.devices.move_backward()

            if self.random or self.trial_num > 30:
                self.update_probabilities()

            times[t_idx] = 'NaN'
            t_idx += 1  # 'noise_onset'
            times[t_idx] = time.perf_counter()  # trial_end
            events += [perfect] + result + [early] + lick + times

            if not self.testing:
                self.save(events)
            self.endTrialSignal.emit()
            if self.testing:
                print('by stimulus:\n', self.performance_stimulus)
                print('overall\n', self.performance_overall)
                print('Events:\n', events)
                print('Licking:\n', self.licking_export)
                print(1, len(result), 1, len(lick))  # 1 was early
            self.licking_export = []
            if self.refresh:
                self.refresh_metrics()
                self.refreshSignal.emit()
                self.refresh = False

    def motor_test(self, ix):
        # self.motors[ix].move_velocity(2)
        # self.motors[ix].move_by(10)
        self.motors[ix].move_to(self.motors[ix].position+self.motor_step)
        print('max', self.motors[ix].get_velocity_parameter_limits())  # max accel, max vel
        print('current', self.motors[ix].get_velocity_parameters())  # min vel, current accel, current max vel
        time.sleep(1)
        # self.motors[ix].move_velocity(1)
        # self.motors[ix].move_by(10)
        self.motors[ix].move_to(self.motors[ix].position-self.motor_step)
        # self.motor.move_home()
        print('posn', self.motors[ix].position)

    def push_water(self):
        self.correct_choice = 0
        self.deliver_water(0)
        self.correct_choice = 1
        self.deliver_water(0)

    def test_odors(self):
        self.trial_type = 0
        self.run_odor(0)
        self.run_odor(1)
        self.trial_type = 3
        self.run_odor(0)
        self.run_odor(1)

if __name__ == '__main__':
    devices = Devices()
    dmsModel = DMSModel(devices, testing=False)
    # dmsModel.push_water()
    # dmsModel.test_odors()
    # model.motor_test(1)
    dmsModel.shut_down()
