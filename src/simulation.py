from itertools import combinations
from typing import Iterable

from src.person import Person


class Simulation:
    color = tuple[float, float, float]
    frame = tuple[list[float], list[float], list[color]]

    population_size: int
    initial_sick: int
    population: list[Person]
    frames: list[frame]

    def __init__(self, population_size: int, initial_sick: int = 1, number_of_frames: int = 30,
                 person_kwargs: dict = None):
        person_kwargs = {} if person_kwargs is None else person_kwargs
        self.frames = []
        self.initial_sick = initial_sick
        self.population_size = population_size
        self.population = [Person(**person_kwargs) for x in range(population_size)]
        self.contact_radius = 0.2
        self.squared_contact_radius = self.contact_radius ** 2
        for idx in range(initial_sick):
            self.population[idx].get_sick()
        self.number_of_frames = number_of_frames
        self.generate_frames(number_of_frames)

    def find_all_interactions(self) -> set[tuple[Person, Person]]:
        """ Finds all interactions between 2 agents, ignores order in which agents appear. """
        contacts = set()
        for person_1, person_2 in combinations(self.population, 2):
            distance = self.calculate_squared_euclidean_distance(person_1.get_position(),
                                                                 person_2.get_position())
            if distance <= self.squared_contact_radius:
                contacts.add((person_1, person_2))
        return contacts

    @staticmethod
    def find_possible_infections(contacts: set[tuple[Person, Person]]) -> Iterable[Person]:
        """ Finds all interactions in which one Person is sick. """
        # TODO introduction of personal protection for sick (if prob > value yield else pass) saved by individual protection case
        for person_1, person_2 in contacts:
            if person_1.can_get_infected() and person_2.can_infect():
                yield person_1
            elif person_1.can_infect() and person_2.can_get_infected():
                yield person_2

    @staticmethod
    def calculate_squared_euclidean_distance(first: tuple[float, float],
                                             second: tuple[float, float]) -> float:
        return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2

    def generate_frames(self, number_of_frames: int) -> None:
        """ Generates given number of frames of the simulation. """
        self.save_frame(*self.get_population_position())
        for frame in range(number_of_frames):
            self.update_population()
            self.save_frame(*self.get_population_position())

    def update_population(self) -> None:
        """ Updates position and health status for each person in the population. """
        for person in self.population:
            person.move()
        interactions = self.find_all_interactions()
        possible_infections = set(self.find_possible_infections(interactions))
        for idx, person in enumerate(possible_infections):
            person.get_infected()

    def get_population_position(self) -> frame:
        """ Get current x, y coordinates of each person and appropriate color depending on the health status. """
        population_description = ((*person.get_position(), person.get_color()) for person in
                                  self.population)
        return tuple(zip(*population_description))

    def save_frame(self, x: list[float], y: list[float], c: list[color]) -> None:
        """ Adds a single frame representing current state of the simulation to the record. """
        self.frames.append((x, y, c))

    def get_frame(self, frame_index: int = -1) -> frame:
        """ Get selected frame of the simulation. """
        if frame_index not in range(len(self.frames)):
            frame_index = -1
        return self.frames[frame_index]

    def __iter__(self):
        return iter(self.frames)

    def __getitem__(self, frame_index) -> frame:
        return self.frames[frame_index]
