from math import sqrt

class Sensor:
    def __init__(self, name, awake, energy, position):
        self.name = name
        self.awake = awake
        self.energy = energy
        self.position = position
    
    def transmit_to(self, other_sensor):
        self.energy = self.energy - Sensor.tx_energy(self, other_sensor)

    def sleep(self):
        idle_energy = 0.1E-6
        self.energy = self.energy - idle_energy

    @staticmethod
    def highest_energy(sensor_list, k = 1):
        energies = [sensor.energy for sensor in sensor_list]
        return sorted(energies)[-k]
    
    @staticmethod
    def distance(first_sensor, second_sensor):
        x_delta = first_sensor.position[0] - second_sensor.position[0]
        y_delta = first_sensor.position[1] - second_sensor.position[1]
        return sqrt((x_delta**2) + (y_delta**2))

    @staticmethod
    def tx_energy(first_sensor, second_sensor):
        e_elec = (17.4E-3)/3600
        # l = 50 * 8
        l = 50
        e_amp = 1
        d = Sensor.distance(first_sensor, second_sensor)
        # energy_cost = e_elec * l + e_amp * l * (d ** 2)
        energy_cost = e_elec * l + e_elec * d
        return energy_cost