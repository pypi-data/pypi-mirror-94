import threading
from .data import PyForPy


class RE21mini:

    def __init__(self):
        # for user
        self.right_motor_speed = 0.0
        self.left_motor_speed = 0.0
        self.back_motor_speed = 0.0

        self.lift_motor_speed = 0.0
        self.angle_to_big = 0.0
        self.dir_to_plates = 0.0

        self.right_motor_enc = 0.0
        self.left_motor_enc = 0.0
        self.back_motor_enc = 0.0
        self.lift_motor_enc = 0.0

        self.reset_right_motor_enc = False
        self.reset_left_motor_enc = False
        self.reset_back_motor_enc = False
        self.reset_lift_motor_enc = False

        self.reset_gyro = False

        self.button_ems = False
        self.button_start = False
        self.button_limit = False

        self.right_us = 0.0
        self.left_us = 0.0
        self.right_ir = 0.0
        self.left_ir = 0.0
        self.gyro = 0.0

        self.bytes_from_camera = None

        # for dev
        self.__connected = False

        port_motors = 65432
        port_oms = 65433
        port_resets = 65434
        port_encoders = 65435
        port_sensors = 65436
        port_buttons = 65437
        port_camera = 65438

        self.__talk_motors = PyForPy.TalkPort(port_motors)
        self.__talk_oms = PyForPy.TalkPort(port_oms)
        self.__talk_resets = PyForPy.TalkPort(port_resets)
        self.__listen_encoders = PyForPy.ListenPort(port_encoders)
        self.__listen_sensors = PyForPy.ListenPort(port_sensors)
        self.__listen_buttons = PyForPy.ListenPort(port_buttons)
        self.__listen_camera = PyForPy.ListenPort(port_camera, True)

    def connect(self):
        self.__connected = True
        client_thread = threading.Thread(target=self.__connect, args=())
        client_thread.start()

    def __connect(self):
        self.__talk_motors.start_talking()
        self.__talk_oms.start_talking()
        self.__talk_resets.start_talking()
        self.__listen_encoders.start_listening()
        self.__listen_sensors.start_listening()
        self.__listen_buttons.start_listening()
        self.__listen_camera.start_listening()
        local_exit = True
        while local_exit:
            self.__talk_motors.out_string = PyForPy.ParseChannels.join_float_channel([self.right_motor_speed,
                                                                                      self.left_motor_speed,
                                                                                      self.back_motor_speed])
            self.__talk_oms.out_string = PyForPy.ParseChannels.join_float_channel([self.lift_motor_speed,
                                                                                   self.angle_to_big,
                                                                                   self.dir_to_plates])
            self.__talk_resets.out_string = PyForPy.ParseChannels.join_bool_channel([self.reset_right_motor_enc,
                                                                                     self.reset_left_motor_enc,
                                                                                     self.reset_back_motor_enc,
                                                                                     self.reset_lift_motor_enc,
                                                                                     self.reset_gyro])
            encoders_list = PyForPy.ParseChannels.parse_float_channel(self.__listen_encoders.out_string)
            if len(encoders_list) == 4:
                self.right_motor_enc = encoders_list[0]
                self.left_motor_enc = encoders_list[1]
                self.back_motor_enc = encoders_list[2]
                self.lift_motor_enc = encoders_list[3]
            sensors_list = PyForPy.ParseChannels.parse_float_channel(self.__listen_sensors.out_string)
            if len(sensors_list) == 5:
                self.right_us = sensors_list[0]
                self.left_us = sensors_list[1]
                self.right_ir = sensors_list[2]
                self.left_ir = sensors_list[3]
                self.gyro = sensors_list[4]
            buttons_list = PyForPy.ParseChannels.parse_bool_channel(self.__listen_buttons.out_string)
            if len(buttons_list) == 3:
                self.button_ems = buttons_list[0]
                self.button_start = buttons_list[1]
                self.button_limit = buttons_list[2]
            self.bytes_from_camera = self.__listen_camera.out_bytes
            local_exit = self.__connected

    def disconnect(self):
        self.__connected = False
        self.__talk_motors.stop_talking()
        self.__talk_oms.stop_talking()
        self.__talk_resets.stop_talking()
        self.__listen_encoders.stop_listening()
        self.__listen_sensors.stop_listening()
        self.__listen_buttons.stop_listening()
        self.__listen_camera.stop_listening()
