import time
import numpy as np
import nidaqmx as ni
from nidaqmx.constants import LineGrouping
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
import sys, os, csv, collections
import thorlabs_apt as apt
from utilities import Devices, Options

# np.random.seed(2)
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
    randomChangedSignal = pyqtSignal()
    intReady = pyqtSignal(int)
    intervalTime = pyqtSignal(float)

    def __init__(self, opts, devices):
        super().__init__()
        self.num_trial_types = 4
        self.opts = opts
        self.testing = opts.testing
        # self.cd_ab = opts.cd_ab
        self.moving_ports = opts.forward_moving_ports

        # performance
        self.trial_num = 0
        self.trial_type_history = []
        self.trial_correct_history = []
        self.trial_array = []  # make a single list of (trial number, choice, early)
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
        self.licking_file = ''
        self.run = False
        self.refresh = False

        # Timing - values in seconds
        self.min_licks = 2
        self.cur_stage = 0
        self.elapsed_time = np.zeros(4)  # odor1, delay, odor2, response
        # iti, no lick, odor1, delay, odor2, response, consumption
        if self.opts.testing:
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
        self.early_tracker = []
        self.early_avg = []

        # water output
        self.trials_to_water = 5
        self.water_times = np.array([.06, .06, .05, .05])
        self.give_water = False
        # DAQ output arrays
        self.all_low = [[False] * 8, [False] * 2]
        self.go_cue = list(self.all_low[0])
        self.light = list(self.all_low[0])
        self.siren = list(self.all_low[0])

        self.go_cue[2] = True
        self.light[3] = True
        self.siren[4] = True

        self.blank = list(self.all_low[0])
        self.blank[7] = True

        odor_a = list(self.all_low[0])  # list() can be used to make a copy
        odor_a[5] = True
        odor_a[7] = True

        odor_b = list(self.all_low[0])
        odor_b[6] = True
        odor_b[7] = True

        odor_c = list(self.all_low[1])
        odor_c[0] = True

        odor_d = list(self.all_low[1])
        odor_d[1] = True

        cdab_trials = {0: [odor_c, odor_a],
                       1: [odor_c, odor_b],
                       2: [odor_d, odor_b],
                       3: [odor_d, odor_a]}

        abab_trials = {0: [odor_a, odor_a],
                       1: [odor_a, odor_b],
                       2: [odor_b, odor_b],
                       3: [odor_b, odor_a]}

        self.trial_dict_list = [abab_trials, cdab_trials]

        lw = list(self.all_low[0])
        lw[0] = True
        rw = list(self.all_low[0])
        rw[1] = True

        self.water_daq = [lw, rw]
        self.output = list(self.all_low)
        time.perf_counter()

        self.lickSideCounter = [0] * 2

        self.dev_low = [[False]]
        self.error_noise = list(self.dev_low[0])
        self.error_noise[0] = True

        self.motors = devices.motors
        self.out_tasks = devices.out_tasks
        self.in_task = devices.in_task
        self.dev_out_task_0 = devices.dev_out_task_0
        self.reader = devices.reader
        self.devices = devices
        self.last_trial_plotted = -1

    def update_indicator(self):
        self.prev_indicator = self.indicator.copy()
        if not self.opts.testing:
            self.reader.read_one_sample_multi_line(self.indicator)

        if not np.array_equal(self.indicator, self.prev_indicator):
            self.lickSignal.emit()
            time.sleep(.001)
            self.licking_export.append([time.perf_counter(), int(self.indicator[0]), int(self.indicator[1])])

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
            tmp = self.user_probabilities
        else:
            tmp = self.probabilities

        tmp[self.trial_type] /= 10  # make repeats unlikely
        tmp /= np.sum(tmp)
        trial_type = np.random.choice(4, p=tmp)
        print('old and new trials', self.trial_type, trial_type)
        return trial_type

    def run_interval(self, delay):
        """A generic delay between stages of the task."""
        st = time.perf_counter()
        t = 0
        if self.cur_stage == 0:
            self.output = self.light
            self.write(0)

        while t < delay:
            time.sleep(.001)
            t = time.perf_counter() - st
            self.update_indicator()
            if self.cur_stage == 3:
                # stimulus time is staggered by two indices - only delay uses this function during stimulus
                self.elapsed_time[self.cur_stage - 2] = t

            if self.cur_stage < 5:
                self.intervalTime.emit(t)

        if self.cur_stage == 0:
            self.output = self.all_low[0]
            self.write(0)

    def run_no_lick(self):
        """Delay the trial until the mouse stops licking for a desired time."""
        no_lick = False
        st = time.perf_counter()
        while not no_lick:
            """
            1. check for lick
            2. if lick, restart time
            3. if no lick, check time passed
            """
            time.sleep(.001)
            self.update_indicator()
            if np.sum(self.indicator) > 0:
                st = time.perf_counter()

            t = time.perf_counter() - st
            self.intervalTime.emit(t)
            if t > self.timing[1]:  # no lick time stage 1
                no_lick = True

    def run_odor(self, cue):
        """
        Release odors.
        :param cue: 0 or 1, denoting the odor delivery stage.
        """
        st = time.perf_counter()
        t = 0
        early = 0
        self.output = self.blank
        self.write(0)
        self.output = list(self.trial_dict_list[int(self.opts.cd_ab)][self.trial_type][cue])
        if self.opts.cd_ab:
            self.write(1 - cue)
        else:
            self.write(0)

        while t < self.timing[2 + cue * 2]:
            # cue is 0 (first odor) or 1 (second odor); odor stages are 2 or 4
            time.sleep(.001)
            t = time.perf_counter() - st
            # stimulus time is staggered by two indices
            self.elapsed_time[self.cur_stage - 2] = t
            self.intervalTime.emit(t)
            self.update_indicator()

            if cue == 1 and self.early_lick_check:  # second odor
                if np.sum(self.indicator) > 0 and t < self.early_lick_time:
                    early = 1

        if self.opts.testing:
            pass
            # early = np.random.randint(2)

        self.output = self.all_low[0]
        self.write(0)
        self.output = self.all_low[1]
        self.write(1)
        return early

    def write(self, daq):  # a cleaner function to call
        # self.writer.write_one_sample_multi_line(self.output)
        # determine which daq to use
        if not self.opts.testing:
            self.out_tasks[daq].write(self.output)

    def write_dev_port(self):
        if not self.opts.testing:
            self.dev_out_task_0.write(self.output)

    def determine_choice(self):
        """
        Determine whether the mouse has chosen left or right.
        outputs -
        choice: the decision made by the mouse. 0 is correct, 1 is error, 2 is a switch, 3 is a miss.
        result: a list with length 4 for correct/error/switch/miss. One-hot for the index given by choice.
            For performance updates.
        side: the side chosen by the mouse. -1 for a switch or miss, 0 left, 1 right.
        """
        st = time.perf_counter()
        licks = np.zeros((2, 1))
        active = False
        choice = 3  # miss
        result = [0] * 4
        side = -1
        # choice = 0 - correct, 1 - error, 2 - switch, 3 - miss
        t = 0
        while t <= self.timing[self.cur_stage]:
            time.sleep(.001)
            t = time.perf_counter() - st
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
                    break
                else:
                    choice = 1  # error
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

        self.trial_correct_history.append(choice)
        result[choice] = 1
        return choice, result, side

    def deliver_water(self, early):
        """Deliver water, assuming the right choice was made."""
        st = time.perf_counter()
        early *= self.early_lick_check  # no water penalty if lick check is off
        water_time = self.water_times[self.correct_choice + early * 2]
        self.output = list(self.water_daq[self.correct_choice])
        self.write(0)
        while (time.perf_counter() - st) < water_time:
            self.update_indicator()

        print('water delivered')
        self.output = self.all_low[0]
        self.write(0)

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
            perc_corr = self.performance_stimulus[:, 2] / (self.performance_stimulus[:, 0] + np.finfo(float).eps)
            self.probabilities = self.sum_normalize(1-perc_corr)
        # avg_perc_correct = np.mean(perc_corr)
        # diff = perc_corr - avg_perc_correct
        # diff *= 2 / self.num_trial_types
        # p = np.ones(self.num_trial_types) / self.num_trial_types - diff
        # if np.sum(np.isnan(p)) > 0:
        #     # print("fail")
        #     return
        # else:
        #     # self.probabilities = self.softmax(p)
        #     self.probabilities = self.sum_normalize(p)
        print("Probabilities: ", self.probabilities)

    def prepare_plot_data(self, choice, early):
        self.trial_array.append((self.trial_num, self.trial_type, choice, early))
        self.early_tracker.append(early)
        st = max(0,self.trial_num-30)   
        self.early_avg = np.mean(self.early_tracker[st:])
        tmp = self.trial_correct_history[st:]
        # self.correct_avg.append(np.sum(tmp[tmp == 0]) / len(tmp) * 100)
        self.correct_avg.append(collections.Counter(tmp)[0] / (len(tmp) + np.finfo(float).eps) * 100)
        self.bias.append(self.performance_overall[5, 0] - self.performance_overall[6, 0])

    def update_performance(self, choice, result, early, lick):
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
        x = np.exp(x - np.amax(x))  # normalization to max of 0
        return x / np.sum(x)

    
    @staticmethod
    def sum_normalize(x):
        return x / np.sum(x)

    def run_go_cue(self):
        self.output = self.go_cue
        st = time.perf_counter()
        t = 0
        self.write(0)
        while t < .15:
            time.sleep(.001)
            t = time.perf_counter() - st
            self.update_indicator()

        self.output = self.all_low[0]
        self.write(0)

    def run_error_noise(self):
        self.output = self.error_noise
        st = time.perf_counter()
        t = 0
        self.write_dev_port()
        while t < .5:
            time.sleep(.001)
            t = time.perf_counter() - st
            self.update_indicator()

        self.output = self.dev_low[0]
        self.write_dev_port()

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
            if not self.opts.testing:
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
                                         'L_reward', 'R_reward', 'noise_onset', 'trial_end', 'AA_hi', 'AB_hi', 'BB_hi', 'BA_hi',
                                         'AA_lo', 'AB_lo', 'BB_lo', 'BA_lo', 'left_w ater_time', 'right_water_time', 'early_left_water',
                                         'early_right_water'])

                        self.water_times

                    with open(self.licking_file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['timestamp', 'left', 'right'])

            time.sleep(.001)  # need sleep time for graph
            self.elapsed_time *= 0
            self.choose_next_trial()

            self.correct_choice = self.trial_type % 2
            self.trial_type_history.append(self.trial_type)
            self.trial_type_progress[1] += 1
            self.startTrialSignal.emit()

            events = [self.trial_num, self.trial_type]
            times = ['NaN'] * 13

            # trial structure
            # print('iti')
            self.cur_stage = 0
            t_idx = 0
            times[t_idx] = time.perf_counter()  # iti start
            t_idx += 1
            iti = self.timing[self.cur_stage] + self.timeout[choice] + \
                  self.early_timeout * early * int(self.early_lick_check)
            self.run_interval(iti)

            # print('no lick')
            self.cur_stage += 1  # 1
            times[t_idx] = time.perf_counter()  # trial start
            t_idx += 1
            self.run_no_lick()

            # print('odor1')
            self.cur_stage += 1  # 2
            times[t_idx:t_idx + 2] = [time.perf_counter()] * 2
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
                # time.sleep(.5)

            self.run_go_cue()

            times[t_idx] = time.perf_counter()  # go tone
            t_idx += 1
            if self.give_water:
                choice, result, side = 0, [0] * 4, self.correct_choice
                result[choice] = 1
                times[t_idx] = time.perf_counter()
            else:
                choice, result, side = self.determine_choice()
                if choice != 3:  # effective lick
                    times[t_idx] = time.perf_counter()

            t_idx += 1
            perfect = np.maximum(result[0] - early, 0)
            lick = [0] * 4  # [left licked, right licked, left correct, right correct]
            if side != -1:
                lick[side] = 1
                self.lickSideCounter[side] += 1

            if trials_to_water_counter >= self.trials_to_water:
                self.give_water = True

            if choice == 0 or self.give_water:
                self.trial_type_progress[0] += 1
                if side >= 0:  # lick made
                    lick[2 + side] = 1
                    times[t_idx + side] = time.perf_counter()  # L/R reward

                trials_to_water_counter = 0
                self.deliver_water(early)
            elif trials_to_water_counter >= self.trials_to_water:  # give water
                trials_to_water_counter = 0
                self.deliver_water(early)
            elif choice == 1 or choice == 2:
                # increase trials-to-water counte
                trials_to_water_counter += 1
                self.run_error_noise()
            else:  # for miss
                trials_to_water_counter += 1

            t_idx += 2
            # consumption time
            self.run_interval(self.timing[-1])  # consumption time is last
            self.update_performance(choice, result, early, lick)
            self.prepare_plot_data(choice, early)

            # remove ports from mouse
            if self.moving_ports:
                self.devices.move_backward()

            if self.random or self.trial_num > 30:
                self.update_probabilities()

            times[t_idx] = 'NaN'
            t_idx += 1  # 'noise_onset'
            times[t_idx] = time.perf_counter()  # trial_end
            human = [self.give_water] + self.hi_bounds.tolist() + self.low_bounds.tolist() + self.water_times
            events += [perfect] + result + [early] + lick + times + human

            self.endTrialSignal.emit()
            self.trial_num += 1
            self.give_water = False
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

    def motor_test(self, ix):
        # self.motors[ix].move_velocity(2)
        # self.motors[ix].move_by(10)
        self.motors[ix].move_to(self.motors[ix].position + self.motor_step)
        print('max', self.motors[ix].get_velocity_parameter_limits())  # max accel, max vel
        print('current', self.motors[ix].get_velocity_parameters())  # min vel, current accel, current max vel
        time.sleep(1)
        # self.motors[ix].move_velocity(1)
        # self.motors[ix].move_by(10)
        self.motors[ix].move_to(self.motors[ix].position - self.motor_step)
        # self.motor.move_home()
        print('posn', self.motors[ix].position)

    def push_water(self):
        self.water_times = [.5, .5, .03, .03]
        self.correct_choice = 0
        self.deliver_water(0)
        self.correct_choice = 1
        self.deliver_water(0)

    def test_odors(self):
        self.trial_type = 0
        self.run_odor(0)
        time.sleep(1)
        self.run_odor(1)
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
