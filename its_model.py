import time
import numpy as np
import pandas as pd
import nidaqmx as ni
import nidaqmx.system, nidaqmx.stream_readers, nidaqmx.stream_writers
from nidaqmx.constants import LineGrouping
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot, QObject
import sys, os, csv, collections
from dms_model_nodaq import DMSModel
import thorlabs_apt as apt

# model = DMSModel(testing=True)

class ITSModel(DMSModel):
    """A Python implementation of the ITS program. Primary changes are the addition of motor control,
    the lack of odor delivery, and the delivery of water for any choice of lick port."""

    def __init__(self, devices, testing=False, moving_ports=True):
        super().__init__(devices, testing, moving_ports)

        # iti, no lick, response, consumption
        if self.testing:
            self.timing = [.1, .1, 0, .1, 0, .1, .1]
            self.save_path = ''
            self.events_file = self.save_path + '/' + self.mouse + '_events'
            self.licking_file = self.save_path + '/' + self.mouse + '_licking'
        else:
            # self.timing = [3, .4, 2, 1]  # standard times
            self.timing = [3, .4, 0, 0, 0, 2, 1]  # standard times
            # timing for delay is index 3

        # choice = 0 - correct, 1 - error, 2 - switch, 3 -
        self.delay_ix = 3
        self.timeout = np.array([0, 3, 3, 0])  # timeout for error/switch
        self.early_timeout = 3
        self.delay_adjust = [.08, .02]  # decrement, increment
        self.delay_increment = .02
        self.delay_decrement = .08
        self.early_lick_pause = 1
        self.delay_max = 1
        self.delay_min = 0
        self.cur_delay = 0
        self.structure = 2

    def its_delay(self):
        """A short delay to prepare the animal not to lick before the go cue."""
        st = time.time()
        t = 0
        early = 0
        while t < self.timing[self.delay_ix]:
            time.sleep(.001)
            t = time.time() - st
            # stimulus time is staggered by two indices
            self.elapsed_time[self.cur_stage - 2] = t
            self.intervalTime.emit(t)
            self.update_indicator()

            if np.sum(self.indicator) > 0 and t < self.early_lick_time:
                early = 1

        return early

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
        # ITS: choice = 0 - any side choice, 1 - lick both at same time, 2 - switch, 3 - miss
        self.output = self.go_cue
        self.write()
        while t < .15:
            time.sleep(.001)
            t = time.time() - st
            self.update_indicator()

        self.output = self.all_low
        self.write()

        t = 0
        # while t <= self.response_window:
        while t <= self.timing[2]:
            time.sleep(.001)
            t = time.time() - st
            self.elapsed_time[self.cur_stage - 2] = t
            self.intervalTime.emit(t)

            self.update_indicator()
            sum_ind = np.sum(self.indicator)
            if np.sum(sum_ind > 1):
                # error, licked both at the same time
                self.performance_overall[1, 0] += 1  # this has no meaning - keep for .txt file
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

            # check for any choice
            if np.sum(licks) == 2:
                side = np.argmax(licks)
                choice = 0
                self.give_water = True
                break

            # Testing
            if self.testing:
                side = np.random.randint(0, 3)
                if side < 2:
                    self.give_water = True
                    choice = 0
                else:
                    side = -1
                    choice = 3  # miss
                break

        self.trial_correct_history.append(choice)
        result[choice] = 1
        return choice, result, side

    @pyqtSlot()
    def run_program(self):
        self.run = True
        self.refresh = False
        choice = 0
        early = 0
        self.random = True
        while self.run:
            # File I/O
            if self.events_file == '':
                print("You must specify a save folder.")
                return

            if not os.path.isfile(self.events_file) and not self.testing:
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
            self.choose_random_trial()
            self.trial_type_progress[1] += 1
            print('trial type', self.trial_type)

            self.trial_num += 1
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
            iti = self.timing[self.cur_stage] + self.timeout[choice] + \
                  self.early_timeout * early * int(self.early_lick_check)
            self.run_interval(iti)
            # self.run_interval(self.timing[self.cur_stage])

            # print('no lick')
            self.cur_stage = 1
            times[t_idx] = time.perf_counter()  # trial start
            t_idx += 1
            self.run_no_lick()
            # self.run_interval(self.timing[self.cur_stage])  # no lick time removed for ITS?

            ## odor deliveries and delay removed for ITS - keep stages for .txt files
            # filler for stages 2, 3, 4 - entry filler for times[t_idx:t_idx + 4]
            times[t_idx:t_idx + 4] = [time.perf_counter()] * 4
            t_idx += 5  # skip idx+4, which is already NaN

            """
            # odor 1 filler
            # self.cur_stage += 1  # 2
            # times[t_idx:t_idx + 2] = [time.perf_counter()] * 2
            # t_idx += 2  # stimulus and odor 1 start

            # delay filler
            # self.cur_stage += 1  # 3
            # times[t_idx] = time.perf_counter()
            # t_idx += 1

            # odor 2 filler
            # self.cur_stage += 1  # 4
            # times[t_idx] = time.perf_counter()
            # t_idx += 1
            # times[t_idx] = 'NaN'
            # t_idx += 1
            """

            # ITS delay
            self.cur_stage = self.delay_ix
            early = self.its_delay()

            # print('response')
            # lick detection/response window
            self.cur_stage = 5
            # move ports to mouse
            if self.moving_ports:
                self.motors[1].move_by(-self.motor_step)

            times[t_idx] = time.perf_counter()  # go tone
            t_idx += 1
            choice, result, side = self.determine_choice()
            if choice != 3:  # effective lick
                times[t_idx] = time.perf_counter()

            t_idx += 1
            perfect = np.maximum(result[0] - early, 0)
            lick = [0] * 4
            if side != -1:
                lick[side] = 1

            if self.give_water:  # aka choice = 0
                lick[2 + side] = 1
                self.trial_type_progress[0] += 1
                times[t_idx + side] = time.perf_counter()  # L/R reward
                self.deliver_water(early)

            t_idx += 2
            self.give_water = False
            self.update_performance(choice, result, early, lick)
            self.prepare_plot_data(choice, early)

            # consumption time
            self.run_interval(self.timing[-1])  # consumption time is last
            # remove ports from mouse
            # remove ports from mouse
            if self.moving_ports:
                self.motors[1].move_by(self.motor_step)

            if early == 1:
                # self.timing[self.delay_ix] = max(self.delay_min, self.timing[self.delay_ix] - self.delay_decrement)
                self.timing[self.delay_ix] = max(self.delay_min, self.timing[self.delay_ix] - self.delay_adjust[0])
            else:
                # self.timing[self.delay_ix] = min(self.delay_max, self.timing[self.delay_ix] + self.delay_increment)
                self.timing[self.delay_ix] = min(self.delay_max, self.timing[self.delay_ix] + self.delay_adjust[1])

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

        # if self.lickSideCounter[0] == 2 or self.lickSideCounter[1] == 2:
        #     sideLicked = self.lickSideCounter.index(max(self.lickSideCounter))
        #     ITS.moveMotor(sideLicked)
        #     self.lickSideCounter = [0] * 2



if __name__ == '__main__':
    model = ITSModel(testing=True)
    # print(model.lickSignal)
    model.run_program()

