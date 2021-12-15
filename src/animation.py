from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src import parameters
from src.simulation import Simulation
import matplotlib
matplotlib.use("Qt5Agg")


def count_people(colors):
    counts = Counter(colors)
    return {
        "healthy": (counts[parameters.HEALTHY_COLOR], parameters.HEALTHY_COLOR),
        "sick": (counts[parameters.SICK_COLOR], parameters.SICK_COLOR),
        "recovered": (counts[parameters.RECOVERED_COLOR], parameters.RECOVERED_COLOR),
    }


simulation = Simulation(100, number_of_frames=50)
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

x, y, c = simulation[0]
scatter = axs[0].scatter(x=x, y=y, c=c)
counts = count_people(c)
plots = {}
for key, (y, c) in counts.items():
    x_data = 0
    y_data = y
    plot, = axs[1].plot(x_data, y_data, c=c, label=key)
    plots[key] = {"data": [y], "plot": plot}


def update_factory(simulation):
    def update(idx):
        idx = idx % simulation.number_of_frames
        x, y, c = simulation[idx]
        scatter.set_offsets(list(zip(x, y)))
        # scatter.set_array(np.array(c))

        for key, (y, _) in count_people(c).items():
            plots[key]["data"].append(y)
            x_data = range(len(plots[key]["data"][0:idx]))
            y_data = plots[key]["data"][0:idx]
            plots[key]["plot"].set_data(x_data, y_data)

        axs[1].set_xlim(0, max(10, idx+1))
        axs[1].figure.canvas.draw()
    return update


update = update_factory(simulation)
anim = animation.FuncAnimation(fig, update, range(50), interval=50)
plt.show()
