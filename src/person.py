import math
import random


class Person:
    x: float
    y: float
    sick: bool
    recovered: bool
    susceptibility: float
    color: tuple[float, float, float]

    HEALTHY_COLOR = (0, 1, 0)
    SICK_COLOR = (1, 0, 0)
    RECOVERED_COLOR = (0.7, 0, 0.7)

    def __init__(self, **kwargs):
        self.x = random.random()
        self.y = random.random()
        self.sick = False
        self.recovered = False
        self.color = type(self).HEALTHY_COLOR
        self.mobility = random.random()
        self.susceptibility = random.random()
        self.recovered_susceptibility = 0
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_sick(self):
        """ Become sick, update corresponding fields. """
        self.sick = True
        self.color = type(self).SICK_COLOR
        self.susceptibility = 0

    def get_color(self):
        """ Get representation of a person health as a corresponding color. """
        return self.color

    def get_position(self) -> tuple[float, float]:
        """ Return current person location. """
        return self.x, self.y

    def recover(self):
        """ Recover from sickness, update corresponding fields. """
        self.sick = False
        self.recovered = True
        self.color = type(self).RECOVERED_COLOR
        self.susceptibility = self.recovered_susceptibility

    def move(self):
        """ Move from previous position to a new one. """
        move_x, move_y = self.get_move_values()
        self.x += move_x
        self.y += move_y
        self.apply_boundary_conditions()

    def apply_boundary_conditions(self):
        """ Check if person did not leave the space of the simulation, if so modifies its position. """
        if self.x > 1:
            self.x -= 1
        if self.x < 0:
            self.x += 1
        if self.y > 1:
            self.y -= 1
        if self.y < 0:
            self.y += 1

    def get_distance_to_travel(self) -> float:
        """ Get distance person will move at the given time step. """
        return random.random() * self.mobility

    @staticmethod
    def get_move_coefficients():
        """ Generate direction in which person will be moved at the given time step. """
        angle = math.radians(random.random() * 360)
        return math.cos(angle), math.sin(angle)

    def get_move_values(self):
        distance_to_move = self.get_distance_to_travel()
        x_coefficient, y_coefficient = self.get_move_coefficients()
        return distance_to_move * x_coefficient, distance_to_move * y_coefficient

    def update(self):
        """ Update status related to disease development. """
        pass

    def can_get_infected(self):
        """ Returns information if given agent can get infected. """
        return not self.sick

    def can_infect(self):
        """ Returns information if given agent can infect others. """
        return self.sick

    def get_infected(self):
        if self.susceptibility >= random.random():
            self.get_sick()
