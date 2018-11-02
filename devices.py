import nidaqmx as ni
from nidaqmx.constants import LineGrouping
import thorlabs_apt as apt
import numpy as np
import time

class Devices:

    def __init__(self, load_moving_ports=True):
        self.out_task_0 = ni.Task()
        self.out_task_0.do_channels.add_do_chan('cDAQ2Mod1/port0/line0:7',
                                              line_grouping=LineGrouping.CHAN_PER_LINE)
        self.writer_0 = ni.stream_writers.DigitalMultiChannelWriter(self.out_task_0.out_stream)
        self.out_task_0.start()

        self.out_task_1 = ni.Task()
        self.out_task_1.do_channels.add_do_chan('cDAQ1Mod1/port0/line0:7',
                                              line_grouping=LineGrouping.CHAN_PER_LINE)
        self.writer_1 = ni.stream_writers.DigitalMultiChannelWriter(self.out_task_1.out_stream)
        self.out_task_1.start()

        self.out_tasks = [self.out_task_0, self.out_task_1]

        self.in_task = ni.Task()
        self.in_task.di_channels.add_di_chan('Dev2/port0/line0:1',
                                             line_grouping=LineGrouping.CHAN_PER_LINE)
        self.reader = ni.stream_readers.DigitalMultiChannelReader(self.in_task.in_stream)
        self.in_task.start()

        # MOTOR
        # if not self.testing:
        devices = apt.list_available_devices()
        motor_0 = apt.Motor(devices[0][1])  # lr motor
        self.motors = [motor_0]
        self.forward_motor_step = 10
        self.sideways_motor_step = .8
        if load_moving_ports:
            # print(devices)
            motor_1 = apt.Motor(devices[1][1])  # forward motor
            self.motors.append(motor_1)

    def move_forward(self):
        self.motors[1].move_by(-self.forward_motor_step)

    def move_backward(self):
        self.motors[1].move_by(self.forward_motor_step)

    def move_left(self):
        self.motors[0].move_by(-self.sideways_motor_step)

    def move_right(self):
        self.motors[0].move_by(self.sideways_motor_step)

    def motor_test(self, ix):
        # self.motors[ix].move_velocity(2)
        # self.motors[ix].move_by(10)
        print('posn', self.motors[ix].position)
        print('min posn', self.motors[ix].get_stage_axis_info())
        print('min posn', self.motors[ix].get_stage_axis_info())
        self.motors[ix].move_to(self.motors[ix].position+10)
        time.sleep(2)

        print('posn', self.motors[ix].position)
        self.motors[ix].move_to(self.motors[ix].position-10)
        print('max', self.motors[ix].get_velocity_parameter_limits())  # max accel, max vel
        print('current', self.motors[ix].get_velocity_parameters())  # min vel, current accel, current max vel
        time.sleep(2)
        # self.motors[ix].move_velocity(1)
        # self.motors[ix].move_by(10)
        print('posn', self.motors[ix].position)
        self.motors[ix].move_to(self.motors[ix].position+10)
        # self.motor.move_home()
        time.sleep(1)
        print('posn', self.motors[ix].position)