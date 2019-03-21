import nidaqmx as ni
from nidaqmx.constants import LineGrouping
import nidaqmx.system, nidaqmx.stream_readers, nidaqmx.stream_writers
import thorlabs_apt as apt
import time

class Options:

    def __init__(self):
        self.forward_moving_ports = True
        self.lr_moving_ports = True
        self.n_daq = 2
        self.cd_ab = False
        self.testing = False


class Devices:

    def __init__(self, opts):
        self.out_task_0 = ni.Task()
        self.out_task_0.do_channels.add_do_chan('cDAQ1Mod1/port0/line0:7',
                                              line_grouping=LineGrouping.CHAN_PER_LINE)
        # self.writer_0 = ni.stream_writers.DigitalMultiChannelWriter(self.out_task_0.out_stream)
        self.out_task_0.start()
        # self.out_tasks = [self.out_task_0]
        self.out_tasks = {'main': self.out_task_0}

        if opts.n_daq == 2:  # if using a box with 2-Daq setup
            self.out_task_1 = ni.Task()
            self.out_task_1.do_channels.add_do_chan('cDAQ2Mod1/port0/line0:1',
                                                line_grouping=LineGrouping.CHAN_PER_LINE)
            # self.writer_1 = ni.stream_writers.DigitalMultiChannelWriter(self.out_task_1.out_stream)
            self.out_task_1.start()
            # self.out_tasks.append(self.out_task_1)
            self.out_tasks['cd'] = self.out_task_1

        self.in_task = ni.Task()
        self.in_task.di_channels.add_di_chan('Dev1/port0/line0:1',
                                             line_grouping=LineGrouping.CHAN_PER_LINE)
        self.reader = ni.stream_readers.DigitalMultiChannelReader(self.in_task.in_stream)
        self.in_task.start()

        # Writer for error noise
        self.dev_out_task_0 = ni.Task()
        self.dev_out_task_0.do_channels.add_do_chan('Dev1/port1/line1',
                                                    line_grouping=LineGrouping.CHAN_PER_LINE)
        self.dev_writer_0 = ni.stream_writers.DigitalMultiChannelWriter(self.dev_out_task_0.out_stream)
        self.dev_out_task_0.start()
        self.out_tasks['dev'] = self.dev_out_task_0

        # MOTOR
        # if not opts.testing:
        devices = apt.list_available_devices()
        motor_0 = apt.Motor(devices[0][1])  # lr motor
        self.motors = [motor_0]
        self.forward_motor_step = 10
        self.sideways_motor_step = .8
        if opts.forward_moving_ports:
            # print(devices)
            motor_1 = apt.Motor(devices[1][1])  # forward motor
            param = motor_1.get_velocity_parameters()
            motor_1.set_velocity_parameters(param[0], 1e3, 200)
            self.motors.append(motor_1)

    def move_forward(self):
        try:
            self.motors[1].move_by(-self.forward_motor_step)
        except:
            message = "Out-of-range position entered to forward motor. The motor must be moved backwards."
            print(message)

    def move_backward(self):
        try:
            self.motors[1].move_by(self.forward_motor_step)
        except:
            message = "Out-of-range position entered to forward motor. The motor must be moved forward."
            print(message)
        
    def move_lr(self, side):
        try:
            if side == 0:  # left
                # self.motors[0].move_by(-self.sideways_motor_step)
                self.motors[0].move_to(self.motors[0].position-self.sideways_motor_step)
            else:
                self.motors[0].move_by(self.sideways_motor_step)
        except:
            message = "Out-of-range position entered to sideways motor. Return the motor to the center."
            print(message)

    def motor_test(self, ix):
        # self.motors[ix].move_velocity(2)
        # self.motors[ix].move_by(10)
        print('posn', self.motors[ix].position)
        print('min posn', self.motors[ix].get_stage_axis_info())
        print('min posn', self.motors[ix].get_stage_axis_info())
        # self.motors[ix].move_to(self.motors[ix].position+1)
        self.motors[ix].move_by(10)
        time.sleep(2)

        print('posn', self.motors[ix].position)
        # self.motors[ix].move_to(self.motors[ix].position-1)
        self.motors[ix].move_by(-10)
        print('max', self.motors[ix].get_velocity_parameter_limits())  # max accel, max vel
        print('current', self.motors[ix].get_velocity_parameters())  # min vel, current accel, current max vel
        time.sleep(2)
        # self.motor.move_home()
        time.sleep(1)
        print('posn', self.motors[ix].position)

if __name__ == '__main__':
    opts = Options()
    devices = Devices(opts)
    devices.motor_test(1)