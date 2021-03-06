from itertools import combinations
from typing import Iterable, Tuple, Set, List

from src.person import Person
from parameters import SimulationParameters
import pandas as pd
from src.utils import count_peeps
import altair as alt


class Simulation:
    color = Tuple[float, float, float]
    frame = Tuple[List[float], List[float], List[color]]

    population_size: int
    initial_sick: int
    population: List[Person]
    frames: List[frame]

    def __init__(self, population_size: int, initial_sick: int = 1, number_of_frames: int = 30,
                 person_kwargs: dict = None, contact_radius: float = 0.5):
        person_kwargs = {} if person_kwargs is None else person_kwargs
        self.frames = []
        self.initial_sick = initial_sick
        self.population_size = population_size
        self.population = [Person(**person_kwargs) for x in range(population_size)]
        self.contact_radius = contact_radius / 1000
        self.squared_contact_radius = self.contact_radius ** 2
        for idx in range(initial_sick):
            self.population[idx].get_sick()
        self.number_of_frames = number_of_frames
        self.generate_frames(number_of_frames)
        self.color_encoding = {(0, 1, 0): "healthy",
                               (1, 0, 0): "sick",
                               (0.7, 0, 0.7): "recovered"}
        self.status_animations = self.get_status_plots()
        self.sim_animations = [plot_animation(self.transform_sim(frame)) for frame in self]
        
    def get_status_plots(self):
        statuses = []
        peeps = []
        for frame in self:
            _, _, c = frame
            people_count = count_peeps(c)
            for status, count in people_count.items():
                statuses.append(status)
                peeps.append(count)
            
        df = pd.DataFrame({"Status": statuses, "Count": peeps}).reset_index()
        df["Step"] = df["index"].apply(lambda x: x // 3)
        status_animations = []
        for i in range(0, len(df["Step"]) + 1):
            _df = df.iloc[0: i * 3]
            status_animations.append(plot_status(_df))
        return status_animations

    def generate_frames(self, number_of_frames: int) -> None:
        """ Generates given number of frames of the simulation. """
        self.save_frame(*self.get_population_position())
        for frame in range(number_of_frames):
            for _ in range(10):
                self.update_population()
            self.save_frame(*self.get_population_position())

    def update_population(self) -> None:
        """ Updates position and health status for each person in the population. """
        for person in self.population:
            person.move()
            person.update_status()
        interactions = self._find_all_interactions()
        possible_infections = set(self._find_possible_infections(interactions))
        for idx, person in enumerate(possible_infections):
            person.get_infected()

    def get_population_position(self) -> frame:
        """ Get current x, y coordinates of each person and appropriate color depending on the health status. """
        population_description = ((*person.get_position(), person.get_color()) for person in
                                  self.population)
        return tuple(zip(*population_description))

    def save_frame(self, x: List[float], y: List[float], c: List[color]) -> None:
        """ Adds a single frame representing current state of the simulation to the record. """
        self.frames.append((x, y, c))

    def _find_all_interactions(self) -> Set[Tuple[Person, Person]]:
        """ Finds all interactions between 2 agents, ignores order in which agents appear. """
        contacts = set()
        for person_1, person_2 in combinations(self.population, 2):
            distance = self._calculate_squared_euclidean_distance(person_1.get_position(),
                                                                  person_2.get_position())
            if distance <= self.squared_contact_radius:
                contacts.add((person_1, person_2))
        return contacts

    @staticmethod
    def _find_possible_infections(contacts: Set[Tuple[Person, Person]]) -> Iterable[Person]:
        """ Finds all interactions in which one Person is sick. """
        # TODO introduction of personal protection for sick (if prob > value yield else pass) saved by individual protection case
        for person_1, person_2 in contacts:
            if person_1.can_get_infected() and person_2.can_infect():
                yield person_1
            elif person_1.can_infect() and person_2.can_get_infected():
                yield person_2

    @staticmethod
    def _calculate_squared_euclidean_distance(first: Tuple[float, float],
                                              second: Tuple[float, float]) -> float:
        return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2

    def __iter__(self):
        return iter(self.frames)

    def __getitem__(self, frame_index: int) -> frame:
        if frame_index not in range(len(self.frames)):
            frame_index = -1
        return self.frames[frame_index]
    
    def transform_sim(self, frame):
        x, y, c = frame
        df = pd.DataFrame({"x": x, "y": y, "c": c})
        df["c"] = df["c"].apply(lambda x: self.color_encoding[x])
        return df


def plot_status(df):
    domain = ["healthy", "sick", "recovered"]
    _range = ["green", "red", "orange"]
    lines = alt.Chart(df).mark_line().encode(
       x="Step",
       y="Count",
       color=alt.Color('Status', scale=alt.Scale(domain=domain, range=_range))
     ).properties(
       width=600,
       height=300
     ) 
    return lines

def plot_animation(df):
    domain = ["healthy", "sick", "recovered"]
    _range = ["green", "red", "orange"]
    chart = alt.Chart(df) \
        .mark_circle(size=60) \
        .encode(x='x', y='y', 
                color=alt.Color('c', scale=alt.Scale(domain=domain, range=_range))) \
        .properties(title="Simulation",
                    width=640, 
                    height=480) \
        .interactive()
    return chart
