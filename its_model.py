import numpy as np
import nidaqmx as ni
from nidaqmx.constants import LineGrouping
from PyQt5.QtCore import *
import os, csv, collections
import thorlabs_apt as apt
from utilities import Devices, Options
from dms_model import DMSModel
# from lickSensorModel import lickSensorModel


class ITSModel(DMSModel):
    """A Python implementation of the ITS program. Primary changes are the addition of motor control,
    the lack of odor delivery, and the delivery of water for any choice of lick port."""

    def __init__(self, opts, devices):
        super().__init__(opts, devices)

        # iti, no lick, response, consumption
        if self.opts.testing:
            self.timing = [100, 100, 0, 100, 0, 100, 100]
            self.save_path = ''
            self.events_file = self.save_path + '/' + self.mouse + '_events'
            self.licking_file = self.save_path + '/' + self.mouse + '_licking'
        else:
            # self.timing = [3, .4, 2, 1]  # standard times
            self.timing = [3000, 400, 0, 0, 0, 2000, 1000]  # standard times
            # timing for delay is index 3

        self.timeout = np.array([0, 3000, 3000, 0])  # timeout for error/switch
        self.early_timeout = 3
        self.delay_adjust = [80, 20]  # decrement, increment
        self.delay_increment = 20
        self.delay_decrement = 80
        self.early_lick_pause = 1000
        self.delay_max = 1000
        self.delay_min = 0
        self.cur_delay = 0
        self.structure = 2
        self.lr_moving_ports = opts.lr_moving_ports
        self.lick_side_counter = np.zeros(2)

    def its_delay(self):
        """A short delay to prepare the animal not to lick before the go cue."""
        ix = self.stage_dict['delay']
        early, t_early = self.run_interval(self.timing[ix], False)
        return early, t_early

    def determine_choice(self):
        """Determine whether the mouse has chosen left or right."""
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

            # check for any choice
            if np.sum(licks) == 2:
                side = np.argmax(licks)  # any choice is correct for its
                choice = 0
                break

            # Testing
            if self.opts.testing:
                choice = np.random.randint(0, 2)
                if choice == 0:
                    side = np.random.randint(0, 2)
                    self.give_water = True
                else:
                    self.give_water = False
                break

        return choice, side

    @pyqtSlot()
    def run_program(self):
        print("running")
        self.run = True
        self.refresh = False
        self.random = True
        choice, early, trials_to_water_counter = 0, 0, 0
        logger_ix = self.logger_ix
        delay_ix = self.stage_ix['delay']
        water_delivered = False

        time = self.time
        time.restart()
        self.indicatorTimer.start()
        while self.run:
            # File I/O
            if self.events_file == '':
                print("You must specify a save folder.")
                return

            if not os.path.isfile(self.events_file) and not self.testing:
                with open(self.events_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.header)

                with open(self.licking_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['timestamp', 'left', 'right'])

            QThread.msleep(1)  # need sleep time for graph
            self.elapsed_time *= 0
            self.choose_next_trial()
            print('hi bound', self.random_hi_bound)
            self.trial_type_progress[1] += 1
            print('trial type', self.trial_type)

            self.startTrialSignal.emit()

            events = [self.trial_num, self.trial_type]
            times = ['NaN'] * 13

            # trial structure

            self.cur_stage = 'iti'
            ix = logger_ix['ITI_start']
            times[ix] = time.elapsed()
            ix = self.stage_dict[self.cur_stage]
            iti = self.timing[ix] + self.timeout[choice] + \
                  self.early_timeout * early * int(self.early_lick_check)
            self.run_iti(iti)

            self.cur_stage = 'no_lick'
            ix = logger_ix['trial_start']
            times[ix] = time.elapsed()
            self.run_no_lick()

            ## odor deliveries removed for ITS - keep stages for .txt files

            # ITS delay
            self.cur_stage = 'delay'
            ix = logger_ix['delay_onset']
            times[ix] = time.elapsed()
            early, t_early = self.its_delay()
            self.early_time_tracker.append(t_early)

            # move lick ports to mouse
            if self.moving_ports:
                self.devices.move_forward()
                self.run_interval(500, False)

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
                    self.deliver_water(early, side)
                    water_delivered = True

                if side >= 0:  # lick made
                    lick[2 + side] = 1
                    self.lick_side_counter[side] += 1

            else:  # error, switch, miss
                trials_to_water_counter += 1
                if choice < 3:
                    ix = logger_ix['noise_onset']
                    times[ix] = time.elapsed()
                    self.run_error_noise()

            result = [0] * 4
            result[choice] = 1
            self.update_performance(choice, result, early, lick)
            self.prepare_plot_data(choice, early)
            print('num trials recorded', len(self.trial_array))

            # consumption time
            self.run_interval(self.timing[-1])  # consumption time is last
            # remove ports from mouse
            if self.moving_ports:
                self.devices.move_backward()

            if early == 1:
                self.timing[delay_ix] = max(self.delay_min, self.timing[delay_ix] - self.delay_adjust[0])
            else:
                self.timing[delay_ix] = min(self.delay_max, self.timing[delay_ix] + self.delay_adjust[1])

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

            print('Lick Counter', self.lick_side_counter)
            print('amax', np.amax(self.lick_side_counter))
            if np.amax(self.lick_side_counter) >= 2 and self.lr_moving_ports:
                side = np.argmax(self.lick_side_counter)  # side licked
                self.devices.move_lr(side)  # move to the opposite side
                self.lick_side_counter *= 0

            self.licking_export = []
            if self.refresh:
                self.refresh_metrics()
                self.refreshSignal.emit()
                self.refresh = False


if __name__ == '__main__':
    model = ITSModel(testing=True)
    # print(model.lickSignal)
    model.run_program()

