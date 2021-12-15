import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from layout import Layout
from src.simulation import Simulation
from src.utils import count_people, get_population_health_status, get_population_health_status_keys

matplotlib.use("Qt5Agg")

# TODO add animation
# TODO add controls for animation
# TODO add restart (generate new simulation and apply current conditions)
# TODO add functionality to sliders
# TODO remove unnecessary buttons (EMPTY)

layout = Layout()
fig = layout.fig
scatter_axis = layout.scatter_axis
scatter_axis.set_xlim(0, 1)
scatter_axis.set_ylim(0, 1)

graph_axis = layout.graph_axis


class Callbacks:

    def __init__(self, scatter_ax: Axes, graph_ax: Axes):
        self.play = False
        self.scatter = None
        self.plots = {}
        self.scatter_ax = scatter_ax
        self.graph_ax = graph_ax
        self.idx = 0
        self.population = 50
        self.sick = 1
        self.steps = 10
        self.contact_range = 0.02
        self.simulation = Simulation(
            self.population, self.sick, self.steps, contact_radius=self.contact_range
        )
        self.init_plots()
        self.update_line_plot_data()

    def init_plots(self):
        x, y, c = self.simulation[0]
        self.scatter = self.scatter_ax.scatter(x=x, y=y, c=c)
        for key, (y, c) in count_people(c).items():
            plot, = self.graph_ax.plot(0, y, c=c, label=key)
            self.plots[key] = {"plot": plot}
        self.graph_ax.set_xlim(0, max(5, self.idx + 1))

    def update_line_plot_data(self):
        health_status_tuples = [get_population_health_status(fc) for _, _, fc in self.simulation]
        health_statuses = zip(get_population_health_status_keys(), zip(*health_status_tuples))
        for key, value in health_statuses:
            self.plots[key]["data"] = value

    def generate(self, _):
        self.simulation = Simulation(
            self.population, self.sick, self.steps, contact_radius=self.contact_range
        )
        self.update_line_plot_data()
        self.graph_ax.set_ylim(0, self.population)
        self.update()

    def next(self, _):
        if self.idx >= self.steps:
            return
        self.idx = self.idx + 1
        self.update()

    def back(self, _):
        if self.idx <= 0:
            return
        self.idx = self.idx - 1
        self.update()

    def play(self, _):
        self.play = True
        if self.idx >= self.steps:
            self.idx = 0
        # TODO Some magic

    def update_population(self, value):
        self.population = value

    def update_sick(self, value):
        self.sick = value

    def update_steps(self, value):
        self.steps = value

    def update_contact_range(self, value):
        self.contact_range = value / 100

    def pause(self, _):
        self.play = False

    def update(self):
        x, y, c = self.simulation[self.idx]
        self.scatter.set_offsets(list(zip(x, y)))
        self.scatter.set_color(np.array(c))

        for key, (y, _) in count_people(c).items():
            x_data = range(self.idx + 1)
            y_data = self.plots[key]["data"][:self.idx+1]
            self.plots[key]["plot"].set_data(x_data, y_data)

        self.graph_ax.set_xlim(0, max(5, self.idx + 1))
        self.scatter_ax.figure.canvas.draw()
        self.graph_ax.figure.canvas.draw()


callbacks = Callbacks(scatter_axis, graph_axis)
layout.button_next.on_clicked(callbacks.next)
layout.button_back.on_clicked(callbacks.back)
layout.button_play.on_clicked(callbacks.play)
layout.button_stop.on_clicked(callbacks.pause)

layout.button_16.on_clicked(callbacks.generate)

layout.button_01.on_changed(callbacks.update_sick)
# layout.button_02.on_changed(call)
# layout.button_03.on_changed()
layout.button_04.on_changed(callbacks.update_contact_range)
layout.button_05.on_changed(callbacks.update_steps)
layout.button_06.on_changed(callbacks.update_population)
# layout.button_11.on_changed()
# layout.button_12.on_changed()

plt.show()
