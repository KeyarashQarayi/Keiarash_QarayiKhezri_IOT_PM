# ************************[TASK -> 01]******************************

import random as R
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


class Device:
    def __init__(self, topic, mqtt_broker='localhost', port=1883):
        self.topic = topic
        self.topic_list = self.topic.split('/')
        self.location = self.topic_list[0]
        self.group = self.topic_list[1]
        self.device_type = self.topic_list[2]
        self.device_name = self.topic_list[3]
        self.mqtt_broker = mqtt_broker
        self.port = port

    def connect_mqtt(self):

        self.mqtt_client = mqtt.client()
        self.mqtt_client.connect(self.mqtt_broker, self.port)

    def setup_gpio(self):

        if self.device_type == 'lamps':
            GPIO.setup(17, GPIO.OUT)

        elif self.device_type == 'doors':
            GPIO.setup(27, GPIO.OUT)

        elif self.device_type == 'fans':
            GPIO.setup(22, GPIO.OUT)

        elif self.device_type == 'camera':
            GPIO.setup(100, GPIO.OUT)

    def turn_on(self):
        self.send_commands('TURN_ON')
        print(f'Your {self.devise_name} is Turn on, Done!')

    def turn_off(self):
        self.send_commands('TURN_OFF')
        print(f'Your {self.devise_name} is Turn off, Done!')

    def send_commands(self, command):
        self.mqtt_client.publish(self.topic, command)
        print('Your command received successfully!')


camera = Device('home/parking/camera/security01')
camera.connect_mqtt()
camera.setup_gpio()
camera.turn_on()
camera.turn_off()

# ************************[TASK -> 02 & 03]******************************


class Device:
    def __init__(self, topic):
        self.topic = topic
        self.device_name = topic.split('/')[-1]
        self.status = "OFF"

    def turn_on(self):
        self.status = "ON"
        print(f'Your {self.devise_name} is Turn on, Done!')

    def turn_off(self):
        self.status = "OFF"
        print(f'Your {self.devise_name} is Turn off, Done!')


class Sensor:
    def __init__(self, topic):
        self.topic = topic
        self.sensor_name = topic.split('/')[-1]
        self.value = 0

    def read_value(self):
        self.value = R.randint(20, 40)
        return self.value


class AdminPanel:
    def __init__(self):
        self.groups = {}

    def create_group(self, group_name):
        if group_name not in self.groups:
            self.groups[group_name] = []
            print(f'This type of group created -> {group_name}')
        else:
            print('Your group name is already exist.')

    def add_device_to_group(self, group_name, device):
        if group_name in self.groups:
            self.groups[group_name].append(device)
            print(f'Your device {device.device_name} added to {group_name}.')
        else:
            print(f'This {group_name} does not exist in groups.')

    def create_device(self, group_name, device_type, name):
        if group_name in self.groups:
            topic = f'home/{group_name}/{device_type}/{name}'
            new_device = Device(topic)
            self.add_device_to_group(group_name, new_device)
            print(f'Your new {new_device.device_name} is added to {
                  group_name} group.')
        else:
            print(f'This {group_name} does not exist in groups.')

    def create_multiple_devices(self, group_name, device_type, number_of_devices):
        if group_name in self.groups:
            for i in range(1, number_of_devices + 1):
                device_name = f'{device_type}{i}'
                topic = f'home/{group_name}/{device_type}/{device_name}'
                new_device = Device(topic)
                self.add_device_to_group(group_name, new_device)
            print(
                f'All {number_of_devices} devices created in group -> {group_name}.')
        else:
            print(f'Your Group {group_name} does not exist yet.')

    def turn_on_all_in_group(self, group_name):
        if group_name in self.groups:
            all_devices = self.groups[group_name]
            for device in all_devices:
                device.turn_on()
            print(f'All devices in group of {group_name} are turned ON.')
        else:
            print(f'Group of {group_name} does not exist.')

    def turn_off_all_in_group(self, group_name):
        if group_name in self.groups:
            all_devices = self.groups[group_name]
            for device in all_devices:
                device.turn_off()
            print(f'All devices in group of {group_name} are turned OFF.')
        else:
            print(f'Group of {group_name} does not exist.')

    def turn_on_all(self):
        for group in self.groups.values():
            for device in group:
                device.turn_on()
        print('All devices in every groups are turnning ON.')

    def turn_off_all(self):
        for group in self.groups.values():
            for device in group:
                device.turn_off()
        print('All devices in every groups are turnning OFF.')

    def get_status_in_group(self, group_name):
        if group_name in self.groups:
            for device in self.groups[group_name]:
                print(f'{device.device_name}: {device.status}')
        else:
            print(f'Group of {group_name} does not founded.')

    def get_status_in_device_type(self, device_type):
        found = False
        for group in self.groups:
            for device in self.groups[group]:
                if device_type in device.topic:
                    print(f'{device.device_name} in group of {
                          group}: {device.status}')
                    found = True
        if not found:
            print(f'No devices founded in {device_type} type.')

    def create_sensor(self, group_name, sensor_type, sensor_name):
        if group_name in self.groups:
            topic = f'home/{group_name}/{sensor_type}/{sensor_name}'
            new_sensor = Sensor(topic)
            self.groups[group_name].append(new_sensor)
            print(f'Your sensor {sensor_name} added to group of {group_name}.')
        else:
            print(f'Group of {group_name} does not exist.')

    def get_status_sensor_in_group(self, group_name):
        if group_name in self.groups:
            print(f'\nStatus of sensors in group "{group_name}":')
            for device in self.groups[group_name]:
                if isinstance(device, Sensor):
                    value = device.read_value()
                    print(f'{device.sensor_name}: {value}')
        else:
            print(f'Group of {group_name} does not exist.')


# *******************************Task-2*********************************
a = AdminPanel()
a.create_group('parking')
a.create_group('bathroom')
a.create_group('room')
a.create_multiple_devices('parking', 'lamps', 40)

# *******************************Task-3*********************************
admine = AdminPanel()
admine.create_group("parking")
admine.create_sensor("parking", "temperature", "T-01")
admine.create_sensor("parking", "humidity", "H-01")
admine.get_status_sensor_in_group("parking")
