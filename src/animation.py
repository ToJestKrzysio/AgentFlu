import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.widgets import TextBox

from src.parameters import AnimationParameters
from src.simulation import Simulation
import matplotlib

from src.utils import count_people

matplotlib.use("Qt5Agg")

simulation = Simulation(AnimationParameters.POPULATION_SIZE,
                        AnimationParameters.INITIAL_SICK,
                        number_of_frames=AnimationParameters.NUMBER_OF_FRAMES)
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
fig = plt.figure(figsize=(15, 5))
scatter_axis = fig.axs([0.05, 0.05, 0.90, 0.30])

x, y, c = simulation[0]
scatter = axs[0].scatter(x=x, y=y, c=c)
counts = count_people(c)
plots = {}
for key, (y, c) in counts.items():
    x_data = 0
    y_data = y
    plot, = axs[1].plot(x_data, y_data, c=c, label=key)
    plots[key] = {"data": [y], "plot": plot}

plt.figlegend()
axs[2].axis('off')


def update_factory(simulation):
    def update(idx):
        idx = idx % simulation.number_of_frames
        x, y, c = simulation[idx]
        scatter.set_offsets(list(zip(x, y)))
        scatter.set_color(np.array(c))

        for key, (y, _) in count_people(c).items():
            plots[key]["data"].append(y)
            x_data = range(len(plots[key]["data"][0:idx]))
            y_data = plots[key]["data"][0:idx]
            plots[key]["plot"].set_data(x_data, y_data)

        axs[1].set_xlim(0, max(10, idx + 1))
        axs[1].figure.canvas.draw()

    return update


update = update_factory(simulation)

# animation
anim = animation.FuncAnimation(fig, update, range(simulation.number_of_frames), interval=15)

# buttons
ax_button = plt.axes([0.7, 0.5, 0.1, 0.05])
grid_button = TextBox(ax_button, "xD")

plt.show()
