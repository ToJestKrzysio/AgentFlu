import matplotlib.pyplot as plt
import matplotlib

from layout import Layout
matplotlib.use("Qt5Agg")

layout = Layout()
fig = plt.figure(figsize=(15, 5))
scatter_axis = fig.add_axes([layout.column_1, layout.plot_y, layout.plot_width, layout.plot_height])
graph_axis = fig.add_axes([layout.column_2, layout.plot_y, layout.plot_width, layout.plot_height])

button_back = fig.add_axes([layout.controls_back, layout.border, layout.controls_width, layout.controls_height])
button_play = fig.add_axes([layout.controls_play, layout.border, layout.controls_width, layout.controls_height])
button_stop = fig.add_axes([layout.controls_stop, layout.border, layout.controls_width, layout.controls_height])
button_next = fig.add_axes([layout.controls_next, layout.border, layout.controls_width, layout.controls_height])

button_01 = fig.add_axes([layout.column_3, layout.button_row_1, layout.button_width, layout.button_height])
button_02 = fig.add_axes([layout.column_3, layout.button_row_2, layout.button_width, layout.button_height])
button_03 = fig.add_axes([layout.column_3, layout.button_row_3, layout.button_width, layout.button_height])
button_04 = fig.add_axes([layout.column_3, layout.button_row_4, layout.button_width, layout.button_height])
button_05 = fig.add_axes([layout.column_3, layout.button_row_5, layout.button_width, layout.button_height])
button_06 = fig.add_axes([layout.column_3, layout.button_row_6, layout.button_width, layout.button_height])

button_11 = fig.add_axes([layout.column_4, layout.button_row_1, layout.button_width, layout.button_height])
button_12 = fig.add_axes([layout.column_4, layout.button_row_2, layout.button_width, layout.button_height])
button_13 = fig.add_axes([layout.column_4, layout.button_row_3, layout.button_width, layout.button_height])
button_14 = fig.add_axes([layout.column_4, layout.button_row_4, layout.button_width, layout.button_height])
button_15 = fig.add_axes([layout.column_4, layout.button_row_5, layout.button_width, layout.button_height])
button_16 = fig.add_axes([layout.column_4, layout.button_row_6, layout.button_width, layout.button_height])

fig.show()
