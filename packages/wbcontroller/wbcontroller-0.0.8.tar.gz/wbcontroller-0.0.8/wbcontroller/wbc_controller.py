from wbcontroller.controller import Supervisor, Node


class Controller:
    def __init__(self, sampling_rate, setup_sensors):
        self.supervisor = Supervisor()
        self.sampling_rate = sampling_rate

        if setup_sensors:
            self.setup_sensors()

    def step(self):
        return self.supervisor.step(self.sampling_rate)

    def get_supervisor(self):
        return self.supervisor

    def get_all_devices(self):
        count = self.supervisor.getNumberOfDevices()

        devices = []

        for i in range(count):
            devices.append(self.supervisor.getDeviceByIndex(i))

        return devices

    def get_devices_by_type(self, node_type):
        devices = self.get_all_devices()
        filtered = []

        for device in devices:
            if device.getNodeType() == node_type:
                filtered.append(device)

        return filtered

    def get_devices_by_type_list(self, list_type):
        devices = self.get_all_devices()
        filtered = []

        for device in devices:
            if list_type.__contains__(device.getNodeType()):
                filtered.append(device)

        return filtered

    def get_position_sensors(self):
        return self.get_devices_by_type(Node.POSITION_SENSOR)

    def get_distance_sensors(self):
        return self.get_devices_by_type(Node.DISTANCE_SENSOR)

    def get_light_sensors(self):
        return self.get_devices_by_type(Node.LIGHT_SENSOR)

    def get_touch_sensors(self):
        return self.get_devices_by_type(Node.TOUCH_SENSOR)

    def get_motors(self):
        return self.get_devices_by_type(Node.ROTATIONAL_MOTOR)

    def get_object_position(self, node_def):
        object_node = self.supervisor.getFromDef(node_def)

        translation_field = object_node.getField("translation")

        return translation_field.getSFVec3f()

    def get_object_rotation(self, node_def):
        object_node = self.supervisor.getFromDef(node_def)

        rotation_field = object_node.getField("rotation")

        return rotation_field.getSFRotation()

    def set_object_position(self, node_def, position):
        object_node = self.supervisor.getFromDef(node_def)

        translation_field = object_node.getField("translation")

        translation_field.setSFVec3f(position)

    def set_object_rotation(self, node_def, rotation):
        object_node = self.supervisor.getFromDef(node_def)

        rotation_field = object_node.getField("rotation")

        rotation_field.setSFRotation(rotation)

    def get_object_velocity(self, node_def):
        return self.supervisor.getFromDef(node_def).getVelocity()

    def setup_sensors(self):
        sensors = self.get_devices_by_type_list([Node.POSITION_SENSOR, Node.DISTANCE_SENSOR, Node.LIGHT_SENSOR, Node.TOUCH_SENSOR])

        for sensor in sensors:
            sensor.enable(self.sampling_rate)

    def setup_motors(self, index_list, pos):
        motors = self.get_motors()

        for index in index_list:
            motors[index].setPosition(pos)

    def set_motor_velocity(self, index, velocity):
        self.get_motors()[index].setVelocity(velocity)

    def get_sensor_value(self, node_type, index):
        sensors = self.get_devices_by_type(node_type)

        return sensors[index].getValue()

    def get_position_sensor_value(self, index):
        return self.get_sensor_value(Node.POSITION_SENSOR, index)

    def get_distance_sensor_value(self, index):
        return self.get_sensor_value(Node.DISTANCE_SENSOR, index)

    def get_light_sensor_value(self, index):
        return self.get_sensor_value(Node.LIGHT_SENSOR, index)

    def get_touch_sensor_value(self, index):
        return self.get_sensor_value(Node.TOUCH_SENSOR, index)
