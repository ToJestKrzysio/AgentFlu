import math
import random


class Person:
    x: float
    y: float
    sick: bool
    recovered: bool
    immunity: float
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
        self.recovery_chance = 0.03
        self.immunity = 0
        self.immunity_decrease_ratio = 0.03
        self.recovered_immunity = 1
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_sick(self):
        """ Become sick, update corresponding fields. """
        self.sick = True
        self.color = type(self).SICK_COLOR
        self.immunity = 1

    def get_color(self):
        """ Get representation of a person health as a corresponding color. """
        return self.color

    def get_position(self) -> tuple[float, float]:
        """ Return current person location. """
        return self.x, self.y

    def update_status(self):
        """ Update status related to disease development. """
        if self.sick:
            self._attempt_recovery()
        else:
            self._reduce_immunity()

    def move(self):
        """ Move from previous position to a new one. """
        move_x, move_y = self._get_move_values()
        self.x += move_x
        self.y += move_y
        self._apply_boundary_conditions()

    def can_get_infected(self) -> bool:
        """ Returns information if given agent can get infected. """
        return not self.sick

    def can_infect(self) -> bool:
        """ Returns information if given agent can infect others. """
        return self.sick

    def get_infected(self) -> None:
        if self.immunity < random.random():
            self.get_sick()

    def _recover(self):
        """ Recover from sickness, update corresponding fields. """
        self.sick = False
        self.recovered = True
        self.color = type(self).RECOVERED_COLOR
        self.immunity = self.recovered_immunity

    def _apply_boundary_conditions(self):
        """ Check if person did not leave the space of the simulation, if so modifies its position. """
        if self.x > 1:
            self.x -= 1
        if self.x < 0:
            self.x += 1
        if self.y > 1:
            self.y -= 1
        if self.y < 0:
            self.y += 1

    def _get_distance_to_travel(self) -> float:
        """ Get distance person will move at the given time step. """
        return random.random() * self.mobility

    @staticmethod
    def _get_move_coefficients():
        """ Generate direction in which person will be moved at the given time step. """
        angle = math.radians(random.random() * 360)
        return math.cos(angle), math.sin(angle)

    def _get_move_values(self):
        """ Returns distances which given person will move in x and y direction. """
        distance_to_move = self._get_distance_to_travel()
        x_coefficient, y_coefficient = self._get_move_coefficients()
        return distance_to_move * x_coefficient, distance_to_move * y_coefficient

    def _attempt_recovery(self) -> None:
        """ Checks if patient will recover at the given time step. """
        if not self.sick:
            return
        if random.random() < self.recovery_chance:
            self._recover()

    def _reduce_immunity(self) -> None:
        """ Reduces immunity of given individual. """
        self.immunity -= self.immunity_decrease_ratio
        if self.immunity < 0:
            self.immunity = 0
