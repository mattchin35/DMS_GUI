import numpy as np
import nidaqmx as ni
from nidaqmx.constants import LineGrouping
from PyQt5.QtCore import *
import os, csv, collections
import thorlabs_apt as apt
from utilities import Devices, Options
# from lickSensorModel import lickSensorModel

# np.random.seed(2)
# Global variables for tuple indexing
EPS = np.finfo(float).eps
ARRAY = 0
DAQ = 1

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
    randomChangedSignal = pyqtSignal()
    intReady = pyqtSignal(int)
    intervalTime = pyqtSignal(float)

    def __init__(self, opts, devices, sensor_model):
        super().__init__()
        self.num_trial_types = 4
        self.opts = opts
        self.testing = opts.testing
        # self.cd_ab = opts.cd_ab
        self.moving_ports = opts.forward_moving_ports
        self.sensors = sensor_model
        # self.indicator = sensor_model.indicator

        # performance
        self.trial_num = 0
        self.trial_type_history = []
        self.trial_correct_history = []
        self.trial_array = []  # make a single list of (trial number, choice, early)
        self.indicator = np.array([[False], [False]])
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
        self.low_bounds = np.ones(self.num_trial_types)
        self.hi_bounds = np.ones(self.num_trial_types) * 3
        self.random_hi_bound = np.random.randint(self.low_bounds[self.trial_type], self.hi_bounds[self.trial_type] + 1)  # starting value
        self.structure = 2  # 0 for CA/CB, 1 for DB/DA, 2 for Full
        self.trial_type_progress = np.zeros(2)  # correct count, total number of trial type seen
        self.probabilities = np.ones(self.num_trial_types) / self.num_trial_types
        self.prev_trial = np.zeros(3)
        self.strict_ub = 20  # number of trials before the program switches trials automatically
        self.correct_choice = 0
        self.min_trial_to_auto = np.array([30, 30])  # number of trials to check before auto change. 0 alt, 1 random

        # User options
        self.random = False
        self.automate = False
        self.use_user_probs = False
        self.user_probabilities = self.probabilities.copy()
        self.save_path = ''  # save location
        self.mouse = ''  # Mouse name
        self.events_file = ''

        self.run = False
        self.refresh = False

        # Timing - values in seconds
        self.min_licks = 2
        self.cur_stage = 0
        self.elapsed_time = np.zeros(4)  # odor1, delay, odor2, response
        # iti, no lick, odor1, delay, odor2, response, consumption

        # Helper dictionaries for readability/
        self.choice_dict = {'correct': 0, 'error': 1, 'switch': 2, 'miss': 3}
        self.stage_dict = {'iti': 0, 'no lick': 1, 'sample': 2, 'delay': 3,
                           'test': 4, 'response': 5, 'consumption': 6}
        self.logger_ix = {'ITI_start': 0, 'trial_start': 1, 'stimulus_start': 2, '1st_odor_onset': 3, 'delay_onset': 4,
                      '2nd_odor_onset': 5, '2nd_delay_onset': 6, 'go_tone': 7, 'effective_lick': 8,
                      'L_reward': 9, 'R_reward': 10, 'noise_onset': 11, 'trial_end': 12}

        outcome_header = ['trial_no.', 'trial_type', 'perfect', 'correct', 'error', 'switch',
                          'miss', 'early_lick', 'left', 'right', 'L_reward', 'R_reward']
        time_header = list(self.logger_ix.keys())
        human_header = ['give_water', 'AA_hi', 'AB_hi', 'BB_hi', 'BA_hi',
                        'AA_lo', 'AB_lo', 'BB_lo', 'BA_lo',
                        'left_water_time', 'right_water_time', 'early_left_water', 'early_right_water']
        self.header = outcome_header + time_header + human_header

        if self.opts.testing:
            # self.timing = [.1] * 7  # for testing
            self.timing = np.array([1000, 400, 500, 1500, 500, 300, 1000])  # standard times
            self.early_timeout = 1e3
            self.timeout = np.array([0, 1000, 1000, 0])  # timeout for correct, error, switch, miss
        else:
            self.timing = np.array([3000, 400, 500, 1500, 500, 300, 1000])  # standard times
            self.early_timeout = 6e3
            self.timeout = np.array([0, 500, 500, 0])  # timeout for correct, error, switch, miss

        self.early_lick_check = False
        self.early_check_time = 0
        self.early_tracker = []
        self.early_avg = []
        self.siren_time = 150
        self.use_siren = False
        self.siren_on = False
        self.early_pause = 0
        self.early_delta = np.array([50, 100])
        self.early_check_bounds = np.array([2500, 0])
        self.early_time_tracker = []
        self.early_performance = np.zeros((5,2))

        # water output
        self.trials_to_water = 5
        self.water_times = np.array([60, 60, 50, 50])
        self.give_water = False
        # DAQ output arrays
        all_low = ([False] * 8, [False] * 2, [False])
        go_cue = list(all_low[0])
        light = list(all_low[0])
        siren = list(all_low[0])
        blank = list(all_low[0])

        go_cue[2] = True
        light[3] = True
        siren[4] = True
        blank[7] = True

        self.go_cue = dict(array=go_cue, daq='main')
        self.light = dict(array=light, daq='main')
        self.siren = dict(array=siren, daq='main')
        self.blank = dict(array=blank, daq='main')

        odor_a = list(all_low[0])  # list() can be used to make a copy
        odor_a[5] = True
        odor_a[7] = True
        self.odor_a = odor_a

        odor_b = list(all_low[0])
        odor_b[6] = True
        odor_b[7] = True
        self.odor_b = odor_b

        odor_c = list(all_low[1])
        odor_c[0] = True
        self.odor_c = odor_c

        odor_d = list(all_low[1])
        odor_d[1] = True
        self.odor_d = odor_d

        odor_a = dict(array=odor_a, daq='main')
        odor_b = dict(array=odor_b, daq='main')
        odor_c = dict(array=odor_c, daq='cd')
        odor_d = dict(array=odor_d, daq='cd')

        cdab_trials = {0: (odor_c, odor_a),
                       1: (odor_c, odor_b),
                       2: (odor_d, odor_b),
                       3: (odor_d, odor_a)}

        abab_trials = {0: (odor_a, odor_a),
                       1: (odor_a, odor_b),
                       2: (odor_b, odor_b),
                       3: (odor_b, odor_a)}

        self.trial_dict_list = (abab_trials, cdab_trials)
        # self.trial_dict = dict(abab=abab_trials, cdab=cdab_trials)

        lw = list(all_low[0])
        rw = list(all_low[0])
        lw[0] = True
        rw[1] = True
        lw = dict(array=lw, daq='main')
        rw = dict(array=rw, daq='main')

        self.water_daq = (lw, rw)
        self.error_noise = dict(array=[True], daq='dev')
        # self.all_low = [dict(array=[False] * 8, daq='main'), dict(array=[False] * 2, daq='cd'),
        #                 dict(array=[False], daq='dev')]
        self.all_low = {'main': dict(array=all_low[0], daq='main'),
                        'cd': dict(array=all_low[1], daq='cd'),
                        'dev': dict(array=all_low[2], daq='dev')}

        # self.output = list(self.all_low)
        self.output = {'main': [False] * 8, 'cd': [False] * 2, 'dev': [False]}
        self.lickSideCounter = [0] * 2

        self.motors = devices.motors
        self.out_tasks = devices.out_tasks
        self.in_task = devices.in_task
        # self.dev_out_task_0 = devices.dev_out_task_0
        self.reader = devices.reader
        self.devices = devices
        self.sensor_model = sensor_model
        self.last_trial_plotted = -1

        self.indicatorTimer = QTimer()
        self.indicatorTimer.setTimerType(Qt.PreciseTimer)
        self.indicatorTimer.callOnTimeout(self.update_indicator)
        self.indicatorTimer.setInterval(10)  # update indicator every 10 milliseconds

        self.time = QTime()
        self.time.start()

    @pyqtSlot()
    def update_indicator(self):
        """Detect the presence of a new lick."""
        prev_indicator = self.indicator.copy()
        if not self.opts.testing:
            self.reader.read_one_sample_multi_line(self.indicator)

        if not np.array_equal(self.indicator, prev_indicator):
            new_lick = (self.indicator - prev_indicator) > 0  # side being newly licked
            if np.sum(new_lick) > 0:
                self.licking_export.append([self.time.elapsed(),
                                            int(new_lick[0]), int(new_lick[1])])
                self.save()

            self.lickSignal.emit()

    def choose_next_trial(self):
        move = False
        if self.random:
            if self.trial_type_progress[1] >= self.random_hi_bound:
                move = True
        elif self.trial_type_progress[1] >= self.strict_ub or self.trial_type_progress[0] >= self.hi_bounds[self.trial_type]:
            move = True
        # potentially move to the next trial type if current progress is greater than minimum
        elif self.trial_type_progress[0] >= self.random_hi_bound:
            move = True

        if move:
            if self.structure == 0:  # AA/AB
                self.trial_type = (self.trial_type + 1) % 2
            elif self.structure == 1:  # BB/BA
                self.trial_type = 2 + ((self.trial_type + 1) % 2)
            else:  # Full
                if self.random:
                    self.trial_type = self.trial_sample()
                else:
                    self.trial_type = (self.trial_type + 1) % 4

            self.trial_type_progress *= 0
            self.random_hi_bound = np.random.randint(self.low_bounds[self.trial_type],
                                                     self.hi_bounds[self.trial_type] + 1)

        if self.automate:
            trange = self.min_trial_to_auto[int(self.random)]
            if self.trial_num >= trange:
                trials_in_range = self.trial_correct_history[(len(self.trial_correct_history) - trange)
                                                             :len(self.trial_correct_history)]
                recent_avg = collections.Counter(trials_in_range)[0] / trange
                if recent_avg >= .8:
                    if self.structure < 2:
                        self.structure = 2
                    elif self.structure == 2:
                        self.random = True  # send signal to update random status
                        self.randomChangedSignal.emit()

                if recent_avg <= .5 and self.random:
                    self.random = False  # send signal to update random status
                    self.randomChangedSignal.emit()

    def trial_sample(self):
        """Sample a trial type from the full set of trials, minus the current trial type."""
        # create a cumulative distribution function
        if self.use_user_probs:
            tmp = self.user_probabilities.copy()
        else:
            tmp = self.probabilities.copy()

        tmp[self.trial_type] /= 5  # make repeats unlikely
        tmp /= np.sum(tmp)
        trial_type = np.random.choice(4, p=tmp)
        print('old and new trials', self.trial_type, trial_type)
        return trial_type

    def run_iti(self, iti):
        self.write_absolute(self.light)
        self.run_interval(iti, odor_period=False)
        self.write_absolute(self.all_low['main'])

    def run_delay(self):
        ix = self.stage_dict['delay']
        early, t_early = self.run_interval(self.timing[ix], odor_period=True, elapsed_ix=1)
        self.write_absolute(self.all_low['main'])
        return early, t_early

    def run_interval(self, delay, odor_period, elapsed_ix=-1):
        """
        A generic delay between stages of the task.
        :param delay: integer length of the interval in milliseconds
        :param odor_period: boolean of whether trial is in sample through test
        :param elapsed_ix: integer index of elapsed time array
        """
        t = QTime()
        t.start()
        elapsed = 0
        if odor_period:
            early, t_early, t_skip = 0, self.early_check_time, 0
            self.siren_on, self.t_siren = False, 0
            intervalTimer = QTimer()
            intervalTimer.setTimerType(Qt.PreciseTimer)
            # emit_time = lambda: self.intervalTime.emit(t.elapsed() - t_skip)
            emit_time = lambda: self.intervalTime.emit(elapsed)
            intervalTimer.callOnTimeout(emit_time)
            intervalTimer.start(10)

        while elapsed < delay:
            if odor_period:
                self.elapsed_time[elapsed_ix] = elapsed

                if self.early_lick_check:
                    loop_early, loop_early, loop_skip = self.early_loop(elapsed)
                    early = max(early, loop_early)
                    t_early = min(t_early, loop_early)
                    t_skip += loop_skip

                if self.siren_on:
                    if elapsed - self.t_siren > self.siren_time:
                        self.siren_on = False
                        self.end_write(self.siren)

            elapsed = t.elapsed() - t_skip

        if odor_period:
            intervalTimer.stop()
            return early, t_early

    def early_loop(self, elapsed):
        """ Check for early licks. For use with sample, delay and test. """
        early, t_early, t_skip = 0, self.early_check_time, 0
        stimulus_time = np.sum(self.elapsed_time)
        if self.early_lick_check:
            if np.sum(self.indicator) > 0 and stimulus_time < self.early_check_time:
                early = 1
                t_early = stimulus_time
                if self.use_siren:
                    self.siren_on = True
                    self.t_siren = elapsed
                    self.write_relative(self.siren)

                if self.early_pause > 0:
                    t_skip = self.run_early_pause()

        return early, t_early, t_skip

    def run_early_pause(self):
        t = QTime()
        t.start()
        elapsed = t.elapsed()
        while elapsed < self.early_pause:
            if self.siren_on and elapsed > self.siren_time:
                self.siren_on = False
                self.end_write(self.siren)
            elapsed = t.elapsed()
        return t.elapsed()

    def run_no_lick(self):
        """Delay the trial until the mouse stops licking for a desired time."""
        no_lick = False
        t = QTime()
        t.start()
        elapsed = 0

        intervalTimer = QTimer()
        intervalTimer.setTimerType(Qt.PreciseTimer)
        emit_time = lambda: self.intervalTime.emit(t.elapsed())
        intervalTimer.callOnTimeout(emit_time)
        intervalTimer.start(10)

        ix = self.stage_dict['no_lick']
        while not no_lick:
            """
            1. check for lick
            2. if lick, restart time
            3. if no lick, check time passed
            """
            # QThread.msleep(1)
            if np.sum(self.indicator) > 0:
                t.restart()
            if elapsed > self.timing[ix]:  # no lick time stage 1
                no_lick = True
            elapsed = t.elapsed()  # value in milliseconds
        intervalTimer.stop()

    def run_odor(self):
        if self.cur_stage == 'sample':
            elapsed_ix = 0
            cue = 0
        else:  # delay
            elapsed_ix = 2
            cue = 1

        self.write_relative(self.blank)
        trial_dict = self.trial_dict_list[int(self.opts.cd_ab)]
        odor = trial_dict[self.trial_type][cue]
        # print(odor)
        self.write_relative(odor)

        ix = self.stage_dict[self.cur_stage]
        early, t_early = self.run_interval(self.timing[ix], True, elapsed_ix)
        self.write_absolute(self.all_low['main'])
        self.write_absolute(self.all_low['cd'])
        return early, t_early

    def determine_choice(self):
        """
        Determine whether the mouse has chosen left or right.
        outputs -
        choice: the decision made by the mouse. 0 is correct, 1 is error, 2 is a switch, 3 is a miss.
        result: a list with length 4 for correct/error/switch/miss. One-hot for the index given by choice.
            For performance updates.
        side: the side chosen by the mouse. -1 for a switch or miss, 0 left, 1 right.
        """
        t = QTime()
        t.start()
        elapsed = 0

        intervalTimer = QTimer()
        intervalTimer.setTimerType(Qt.PreciseTimer)
        emit_time = lambda: self.intervalTime.emit(t.elapsed())
        intervalTimer.callOnTimeout(emit_time)
        intervalTimer.start(10)

        licks = np.zeros((2, 1))
        active = False
        choice = 3  # miss
        side = -1
        # choice = 0 - correct, 1 - error, 2 - switch, 3 - miss
        ix = self.stage_dict['response']
        while elapsed <= self.timing[ix]:
            self.elapsed_time[3] = elapsed
            sum_ind = np.sum(self.indicator)

            # error, licked both at the same time
            if sum_ind > 1:
                self.performance_overall[1, self.correct_choice] += 1
                choice = 1
                break

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
                choice = side == self.correct_choice
                break

            # Testing
            if self.opts.testing:
                choice = np.random.randint(0, 2)
                if choice == 0:
                    side = self.correct_choice
                    self.give_water = True
                else:
                    side = 1 - self.correct_choice
                    self.give_water = False
                break

        return choice, side

    def deliver_water(self, early, side):
        """Deliver water, assuming the right choice was made."""
        early *= self.early_lick_check  # no water penalty if lick check is off
        water_time = self.water_times[side + early * 2]
        water = self.water_daq[side]
        self.write_absolute(water)
        self.run_interval(water_time, False)
        print('water delivered')
        self.write_absolute(self.all_low['main'])

    def shut_down(self):
        for task in self.out_tasks:
            task.stop()
            task.close()
        self.in_task.stop()
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
        self.trial_array = []
        self.correct_avg = []
        self.performance_overall *= 0
        self.performance_stimulus *= 0
        self.early_performance *= 0
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
        self.last_trial_plotted = -1

    def update_probabilities(self):
        if self.trial_num > 30:
            # tr_type = np.array(self.trial_type_history)
            # tr_corr = np.array(self.trial_correct_history) == 0
            # aa = tr_type == 0
            # ab = tr_type == 1
            # bb = tr_type == 2
            # ba = tr_type == 3
            #
            # # st = max(0, self.trial_num-30)
            # # aa_corr = tr_corr * aa
            # # ab_corr = tr_corr * ab
            # # bb_corr = tr_corr * bb
            # # ba_corr = tr_corr * ba
            #
            # aa_corr = tr_corr[aa]
            # if len(aa_corr) > 0:
            #     aa_st = max(len(aa_corr)-30, 0)
            #     aa_p = np.mean(aa_corr[aa_st:])
            # else:
            #     aa_p = 0
            #
            # ab_corr = tr_corr[ab]
            # if len(ab_corr) > 0:
            #     ab_st = max(len(ab_corr)-30, 0)
            #     ab_p = np.mean(ab_corr[ab_st:])
            # else:
            #     ab_p = 0
            #
            # bb_corr = tr_corr[bb]
            # if len(bb_corr) > 0:
            #     bb_st = max(len(bb_corr)-30, 0)
            #     bb_p = np.mean(bb_corr[bb_st:])
            # else:
            #     bb_p = 0
            #
            # ba_corr = tr_corr[ba]
            # if len(ba_corr) > 0:
            #     ba_st = max(len(ba_corr)-30, 0)
            #     ba_p = np.mean(ba_corr[ba_st:])
            # else:
            #     ba_p = 0

            # perc_corr = np.array([aa_p, ab_p, bb_p, ba_p])
            # perc_corr[np.isnan(perc_corr)] = 0
            perc_corr = self.performance_stimulus[:, 2] / (self.performance_stimulus[:, 0] + np.finfo(float).eps)
            self.probabilities = self.sum_normalize(1-perc_corr)
            print("Probabilities: ", self.probabilities)

    def prepare_plot_data(self, choice, early):
        self.trial_array.append((self.trial_num, self.trial_type, choice, early))
        self.early_tracker.append(early)
        st = max(0,self.trial_num-30)   
        self.early_avg.append(np.mean(self.early_tracker[st:]))
        tmp = self.trial_correct_history[st:]
        # self.correct_avg.append(np.sum(tmp[tmp == 0]) / len(tmp) * 100)
        self.correct_avg.append(collections.Counter(tmp)[0] / (len(tmp) + np.finfo(float).eps) * 100)
        self.bias.append(self.performance_overall[5, 0] - self.performance_overall[6, 0])

    def update_performance(self, choice, result, early, lick):
        print(choice, result, early, lick)
        # performance_stimulus
        # rows: num trials, % perfect, %correct, %error, %switch, %miss, %early
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
        # cols: correct, error, switch, miss, early_lick, left, right, l reward, r reward
        # left column numbers, right column percent
        self.performance_overall[:, 0] += np.array(result + [early] + lick)
        self.performance_overall[:, 1] = self.performance_overall[:, 0] / (self.trial_num + EPS)

        # early lick performance
        early_time = np.array(self.early_time_tracker)
        tr_type = np.array(self.trial_type_history)
        tr = tr_type == self.trial_type
        self.early_performance[1, self.trial_type] = np.mean(early_time[tr])
        self.early_performance[0, self.trial_type] = self.early_check_time - self.early_performance[1, self.trial_type]
        # self.early_performance[-1, 1] = np.mean(early_time)
        self.early_performance[-1] = np.mean(self.early_performance[:4], axis=0)

    @staticmethod
    def softmax(x):
        x = np.exp(x - np.amax(x))  # normalization to max of 0
        return x / np.sum(x)

    @staticmethod
    def sum_normalize(x):
        return x / (np.sum(x) + EPS)

    def run_go_cue(self):
        self.write_absolute(self.go_cue)
        self.run_interval(150, False)
        self.write_absolute(self.all_low['main'])

    def run_error_noise(self):
        self.write_absolute(self.error_noise)
        self.run_interval(500, False)
        self.write_absolute(self.all_low['dev'])

    def write_absolute(self, output):
        # output overwriting all present outputs
        L, daq = output['array'], output['daq']
        # L, daq = output
        self.output[daq] = list(L)
        if not self.opts.testing:
            self.out_tasks[daq].write(self.output[daq])

    def write_relative(self, output):
        # write an output without affecting other processes
        L, daq = output['array'], output['daq']
        # L, daq = output
        self.output[daq] = [x or y for x, y in zip(self.output[daq], L)]
        if not self.opts.testing:
            # print(self.output[daq])
            self.out_tasks[daq].write(self.output[daq])

    def end_write(self, output):
        # end the output of a specific signal without interrupting other processes.
        L, daq = output['array'], output['daq']
        # L, daq = output
        not_output = [not x for x in L]
        end_signal = [x and y for x, y in zip(self.output[daq], not_output)]
        self.output[daq] = end_signal
        if not self.opts.testing:
            self.out_tasks[daq].write(self.output[daq])

    @pyqtSlot()
    def run_program(self):
        """Run the training program until the controller stops it."""
        # set the next trial
        # if self.automate:
        # check the percent correct

        self.run = True
        self.refresh = False
        choice, early, trials_to_water_counter = 0, 0, 0
        logger_ix = self.logger_ix
        water_delivered = False

        time = self.time
        time.restart()
        self.indicatorTimer.start()
        while self.run:
            # File I/O
            if not self.opts.testing:
                if self.events_file == '':
                    print("You must specify a save folder.")
                    return

                if not os.path.isfile(self.events_file):
                    with open(self.events_file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(self.header)

                    with open(self.licking_file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['timestamp', 'left', 'right'])

            QThread.msleep(1)  # need sleep time for graph
            self.elapsed_time *= 0
            self.choose_next_trial()

            self.correct_choice = self.trial_type % 2
            self.trial_type_history.append(self.trial_type)
            self.trial_type_progress[1] += 1
            self.startTrialSignal.emit()

            events = [self.trial_num, self.trial_type]
            times = ['NaN'] * len(self.logger_ix)

            ## Trial structure ##

            self.cur_stage = 'iti'
            ix = logger_ix['ITI_start']
            times[ix] = time.elapsed()
            ix = self.stage_dict[self.cur_stage]
            iti = self.timing[ix] + self.timeout[choice] + \
                  self.early_timeout * early * int(self.early_lick_check)
            self.run_interval(iti)

            self.cur_stage = 'no_lick'
            ix = logger_ix['trial_start']
            times[ix] = time.elapsed()
            self.run_no_lick()

            self.cur_stage = 'sample'
            sample_st = time.elapsed()
            ix = logger_ix['stimulus_start']
            times[ix] = sample_st
            ix = logger_ix['1st_odor_onset']
            times[ix] = sample_st
            early_sample, t_early_sample = self.run_odor()

            self.cur_stage = 'delay'
            ix = logger_ix['delay_onset']
            times[ix] = time.elapsed()
            early_delay, t_early_delay = self.run_delay()

            self.cur_stage = 'test'
            ix = logger_ix['2nd_odor_onset']
            times[ix] = time.elapsed()
            early_test, t_early_test = self.run_odor()

            early = np.amax([early_sample, early_delay, early_test])
            t_early = np.amin([t_early_sample, t_early_delay, t_early_test])
            self.early_time_tracker.append(t_early)

            # move lick ports to mouse
            if self.moving_ports:
                self.devices.move_forward()
                self.run_interval(500, False)

            # 2nd delay onset is left as Nan

            if trials_to_water_counter >= self.trials_to_water:
                self.give_water = True

            ix = logger_ix['go_tone']
            times[ix] = time.elapsed()
            self.run_go_cue()

            if self.correct_choice == 0:
                water_ix = logger_ix['L_reward']
            else:
                water_ix = logger_ix['R_reward']

            self.cur_stage = 'response'
            if self.give_water:
                times[water_ix] = time.elapsed()
                self.deliver_water(early, self.correct_choice)
                water_delivered = True

            ix = logger_ix['effective_lick']
            choice, side = self.determine_choice()
            if choice != 3:  # effective lick
                times[ix] = time.elapsed()

            perfect = int(choice == 0 and early == 0)
            lick = [0] * 4  # [left licked, right licked, left correct, right correct]
            if side != -1:
                lick[side] = 1

            if choice == 0:  # correct
                self.trial_type_progress[0] += 1
                trials_to_water_counter = 0
                if not water_delivered:
                    times[water_ix] = time.elapsed()
                    self.deliver_water(early, self.correct_choice)
                    water_delivered = True

                if side >= 0:  # lick made
                    lick[2 + side] = 1

            else:  # error, switch, miss
                trials_to_water_counter += 1
                if choice < 3:
                    ix = logger_ix['noise_onset']
                    times[ix] = time.elapsed()
                    self.run_error_noise()

            # consumption time
            self.run_interval(self.timing[-1], False)  # consumption time is last

            # remove ports from mouse
            if self.moving_ports:
                self.devices.move_backward()

            self.trial_correct_history.append(choice)

            if self.early_lick_check:
                sign = early * -2 + 1
                check_time = self.early_check_time + sign * self.early_check_bounds[early]
                check_time = max(min(check_time, self.early_check_bounds[0]), self.early_check_bounds[1])
                self.early_check_time = check_time

            result = [0] * 4
            result[choice] = 1
            self.update_performance(choice, result, early, lick)
            self.prepare_plot_data(choice, early)
            if self.random or self.trial_num > 30:
                self.update_probabilities()

            ix = logger_ix['trial_end']
            times[ix] = time.elapsed()
            human = [self.give_water] + self.hi_bounds.tolist() + self.low_bounds.tolist() + self.water_times.tolist()
            events += [perfect] + result + [early] + lick + times + human

            self.endTrialSignal.emit()
            self.trial_num += 1
            self.give_water = False
            water_delivered = False
            if self.opts.testing:
                print('by stimulus:\n', self.performance_stimulus)
                print('overall\n', self.performance_overall)
                print('Events:\n', events)
                print('Licking:\n', self.licking_export)
                print(1, len(result), 1, len(lick))  # 1 was early
            else:
                self.save(events)

            self.licking_export = []
            if self.refresh:
                self.refresh_metrics()
                self.refreshSignal.emit()
                self.refresh = False

    def stop(self):
        self.run = False
        self.indicatorTimer.stop()

    def motor_test(self, ix):
        # self.motors[ix].move_velocity(2)
        # self.motors[ix].move_by(10)
        self.motors[ix].move_to(self.motors[ix].position + self.motor_step)
        print('max', self.motors[ix].get_velocity_parameter_limits())  # max accel, max vel
        print('current', self.motors[ix].get_velocity_parameters())  # min vel, current accel, current max vel
        QThread.sleep(1)
        # self.motors[ix].move_velocity(1)
        # self.motors[ix].move_by(10)
        self.motors[ix].move_to(self.motors[ix].position - self.motor_step)
        # self.motor.move_home()
        print('posn', self.motors[ix].position)

    def push_water(self):
        self.water_times = [50, 50, 30, 30]
        self.deliver_water(0, 0)
        self.deliver_water(0, 1)

    def test_odors(self):
        self.trial_type = 0
        self.cur_stage = 'sample'
        self.run_odor()
        QThread.sleep(1)
        self.cur_stage = 'test'
        self.run_odor()
        # self.trial_type = 3
        # self.run_odor(0)
        # self.run_odor(1)


if __name__ == '__main__':
    opts = Options()
    devices = Devices(opts)
    dmsModel = DMSModel(opts, devices)
    dmsModel.push_water()
    # dmsModel.test_odors()
    # model.motor_test(1)
    dmsModel.shut_down()
