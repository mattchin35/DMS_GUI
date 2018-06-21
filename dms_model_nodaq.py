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

TESTING = True
if TESTING:
    USE_DAQ = False
else:
    USE_DAQ = True

class DMSModel(QObject):
    """
    Model for the DMS training program. Will be adjusted to abstract
    repeated functions when moving to other programs.
    """

#   Signals
    lickSignal = pyqtSignal()
    startTrialSignal = pyqtSignal()
    endTrialSignal = pyqtSignal()
    endProgramSignal = pyqtSignal()
    intReady = pyqtSignal(int)
    intervalTime = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.num_trial_types = 4

        # performance
        self.trial_num = 0
        self.trial_type_history = []
        self.trial_correct_history = []
        self.trialArray = []
        self.allChoices = []
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
        self.correct_trials = [[],[]]
        self.error_trials = [[],[]]
        self.switch_trials = [[],[]]
        self.miss_trials = [[],[]]

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
        self.total_time = np.zeros(4)  # odor1, delay, odor2, response
        # iti, no lick, odor1, delay, odor2, response, consumption
        if TESTING:
            self.timing = [.1] * 7  # for testing
        else:
            self.timing = [3, .4, .5, 1.5, .5, 3, 1]  # standard times
        self.early_lick_time = 0
        self.early_timeout = 6
        self.timeout = np.array([0, 5, 5, 0])  # timeout for error/switch

        # water output
        self.trials_to_water = 5
        self.water_times = [.06, .06]
        self.give_water = False

        # make an array for digital output
        self.do = np.array([False] * 8)
        self.do = self.do[:, np.newaxis]

        # DAQ setup
        if USE_DAQ:
            # system = ni.system.System.local()
            self.out_task = ni.Task()
            self.out_task.do_channels.add_do_chan('cDAQ1Mod1/port0/line0:7',
                                                  line_grouping=LineGrouping.CHAN_PER_LINE)
            self.writer = ni.stream_writers.DigitalMultiChannelWriter(self.out_task.out_stream)
            self.out_task.start()

            self.in_task = ni.Task()
            self.in_task.di_channels.add_di_chan('Dev1/port0/line0:1',
                                                 line_grouping=LineGrouping.CHAN_PER_LINE)
            self.reader = ni.stream_readers.DigitalMultiChannelReader(self.in_task.in_stream)
            self.in_task.start()

        # make an array for digital output
        self.do = np.array([False] * 8)
        self.do = self.do[:, np.newaxis]

        # DAQ output arrays
        self.all_low = [False] * 8
        self.go_cue = [False] * 8
        self.light = [False] * 8
        self.siren = [False] * 8

        self.go_cue[2] = True
        self.light[3] = True
        self.siren[4] = True

        odor_a = list(self.all_low)
        odor_a[5] = True
        odor_a[7] = True

        odor_b = list(self.all_low)
        odor_b[6] = True
        odor_b[7] = True

        self.trial_dict = {0: [odor_a, odor_a],
                           1: [odor_a, odor_b],
                           2: [odor_b, odor_b],
                           3: [odor_b, odor_a]}

        lw = list(self.all_low)
        lw[0] = True
        rw = list(self.all_low)
        rw[1] = True

        self.water_daq = [lw, rw]
        self.output = [False] * 8
        time.perf_counter()

    def update_indicator(self):
        self.prev_indicator = self.indicator.copy()
        if USE_DAQ:
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
        while t < delay:
            time.sleep(.001)
            t = time.time() - st
            self.update_indicator()
            if self.cur_stage == 0:
                self.output = self.light
                self.write()
            elif self.cur_stage == 3:
                # stimulus time is staggered by two indices - only delay uses this function during stimulus
                self.total_time[self.cur_stage - 2] = t

            if self.cur_stage < 5:
                self.intervalTime.emit(t)

        self.output = self.all_low
        self.write()

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
        """Release odors."""
        st = time.time()
        t = 0
        # while t < self.odor_times[cue]:
        early = [0]
        while t < self.timing[2 + cue*2]:
            # cue is 0 or 1; odor stages are 2 or 4
            time.sleep(.001)
            t = time.time() - st
            # stimulus time is staggered by two indices
            self.total_time[self.cur_stage - 2] = t
            self.intervalTime.emit(t)
            self.output = list(self.trial_dict[self.trial_type][cue])
            self.write()
            self.update_indicator()

            if cue == 1:
                if np.sum(self.indicator) > 0 and t < self.early_lick_time:
                    early = [1]

        self.output = list(self.all_low)
        self.write()
        return early

    def write(self):  # a cleaner function to call
        # self.writer.write_one_sample_multi_line(self.output)
        if USE_DAQ: self.out_task.write(self.output)

    def determine_choice(self):
        """Determine whether the mouse has chosen left or right."""
        st = time.time()
        t = 0
        licks = np.zeros((2, 1))
        active = False
        choice = 3  # miss
        result = [0] * 4
        side = -1
        # choice = 0 - correct, 1 - error, 2 - switch, 3 - miss
        self.output = self.go_cue
        while t < .15:
            time.sleep(.001)
            self.write()
            t = time.time() - st
            self.update_indicator() 

        self.output = self.all_low
        self.write()

        t = 0
        # while t <= self.response_window:
        while t <= self.timing[self.cur_stage]:
            time.sleep(.001)
            t = time.time() - st
            self.total_time[self.cur_stage - 2] = t
            self.intervalTime.emit(t)

            self.update_indicator()
            sum_ind = np.sum(self.indicator)
            if np.sum(sum_ind > 1):
                # error, licked both at the same time
                self.overall[1, self.correct_choice] += 1
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
            if TESTING:
                choice = random.randint(0, 3)
                if choice == 0:
                    self.give_water = True
                else:
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

    def deliver_water(self):
        """Deliver water, assuming the right choice was made."""
        st = time.time()
        while (time.time() - st) < self.water_times[self.correct_choice]:
            self.update_indicator()
            self.output = list(self.water_daq[self.correct_choice])
            self.write()
        print('water delivered')
        self.output = list(self.all_low)
        self.write()
        # self.out_task.write()

    def shut_down(self):
        self.out_task.stop()
        self.in_task.stop()
        self.out_task.close()
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
        self.allChoices = []
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
        perc_corr = self.performance_stimulus[:,2] / self.performance_stimulus[:,0]
        avg_perc_correct = np.mean(perc_corr)
        diff = perc_corr - avg_perc_correct
        diff *= 2 / self.num_trial_types
        p = np.ones(self.num_trial_types) / self.num_trial_types - diff
        if np.sum(np.isnan(p)) > 0:
            return
        else:
            self.probabilities = self.softmax(p)
            print("Probabilities: ", self.probabilities)

    def prepare_plot_data(self, choice):
        if choice == 0:
            self.correct_trials[0].append(self.trial_num)
            self.correct_trials[1].append(self.trial_type)
        elif choice == 1:
            self.error_trials[0].append(self.trial_num)
            self.error_trials[1].append(self.trial_type)
        elif choice == 2:
            self.switch_trials[0].append(self.trial_num)
            self.switch_trials[1].append(self.trial_type)
        else:  # 3
            self.miss_trials[0].append(self.trial_num)
            self.miss_trials[1].append(self.trial_type)

        if self.trial_num < 30:
            tmp = self.trial_correct_history
        else:
            tmp = self.trial_correct_history[-30:]
        # self.correct_avg.append(np.sum(tmp[tmp == 0]) / len(tmp) * 100)
        self.correct_avg.append(collections.Counter(tmp)[0] / len(tmp) * 100)

        self.bias.append(self.performance_overall[5,0] - self.performance_overall[6,0])

    def update_performance(self, choice, result, early, lick):
        # get total number of a result, add 1 and divide by new total trial type
        cnt = self.performance_stimulus[self.trial_type, 2:] * self.performance_stimulus[self.trial_type, 0]
        self.performance_stimulus[self.trial_type, 0] += 1
        cnt[choice] += 1
        self.performance_stimulus[self.trial_type, 2:] = cnt / self.performance_stimulus[self.trial_type, 0]

        tmp = np.sum(self.performance_stimulus, axis=1)
        lr = [tmp[0] + tmp[2], tmp[1] + tmp[3]]

        self.performance_overall[:, 0] += np.array(result + early + lick)
        self.performance_overall[:4, 1] = self.performance_overall[:4, 0] / self.trial_num
        if lr[0] > 0:
            self.performance_overall[5, 1] = self.performance_overall[5, 0] / lr[0]
            self.performance_overall[7, 1] = self.performance_overall[5, 0] / lr[0]

        if lr[1] > 0:
            self.performance_overall[6, 1] = self.performance_overall[6, 0] / lr[1]
            self.performance_overall[8, 1] = self.performance_overall[8, 0] / lr[1]

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
        choice = 0
        early = [0]
        while self.run:
            # File I/O
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
            self.total_time *= 0
            if self.random:
                self.choose_random_trial()
            else:
                self.choose_alternating_trial()

            self.correct_choice = self.trial_type % 2
            self.trial_type_history.append(self.trial_type)
            # print(self.trial_type_history)
            self.trial_type_progress[1] += 1
            self.trial_num += 1
            self.trialArray.append(self.trial_num)
            # self.startTrialSignal.signal.emit()
            self.startTrialSignal.emit()

            events = [self.trial_num, self.trial_type]
            times = ['NaN'] * 13

            # trial structure
            # print('iti')
            self.cur_stage = 0
            t_idx = 0
            times[t_idx] = time.perf_counter()  # iti start
            t_idx += 1
            iti = self.timing[self.cur_stage] + self.timeout[choice] + 6 * early[0]
            self.run_interval(self.timing[self.cur_stage])
            # self.run_interval(iti)

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
            times[t_idx] = 'NaN'  # 2nd delay onset no longer used
            t_idx += 1

            # print('response')
            # lick detection/response window
            self.cur_stage += 1  # 5
            times[t_idx] = time.perf_counter()  # go tone
            t_idx += 1
            choice, result, side = self.determine_choice()
            if choice != 3:  # effective lick
                times[t_idx] = time.perf_counter()

            t_idx += 1
            perfect = [1*result[0] - early[0]]
            lick = [0] * 4
            if side != -1:
                lick[side] = 1

            if self.give_water:  # aka choice = 1
                self.trial_type_progress[0] += 1
                lick[2 + self.correct_choice] = 1
                times[t_idx + self.correct_choice] = time.perf_counter()  # L/R reward
                self.deliver_water()

            t_idx += 2
            self.give_water = False

            self.update_performance(choice, result, early, lick)

            # consumption time
            # self.run_interval(self.consumption_time)
            self.run_interval(self.timing[-1])  # consumption time is last

            self.prepare_plot_data(choice)
            if self.random or self.trial_num > 30:
                self.update_probabilities()

            times[t_idx] = 'NaN'
            t_idx += 1  # 'noise_onset'
            times[t_idx] = time.perf_counter()  # trial_end
            events += perfect + result + early + lick + times
            self.save(events)
            self.endTrialSignal.emit()
            if TESTING:
                print('by stimulus:\n', self.performance_stimulus)
                print('overall\n', self.performance_overall)
                print('Events:\n', events)
                print('Licking:\n', self.licking_export)
                print(len(perfect), len(result), len(early), len(lick))
            self.licking_export = []
            if self.refresh:
                self.refresh_metrics()
                self.refresh = False

if __name__ == '__main__':
    model = DMSModel()
    # model.set_random()
    model.random = True
    model.structure = 2
    model.run_program()
    model.shut_down()

