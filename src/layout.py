import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, Slider


class Layout:

    def __init__(self):
        self.plot_width = 0.25
        self.controls_height = 0.06
        self.controls_width = 0.02
        self.controls_border = 0.02
        self.border = 0.05
        self.plot_y = self.border + self.border + 0.1
        self.plot_height = 1 - self.plot_y - self.border
        self.button_width = 0.1
        self.button_height = 0.05

        self.column_1 = self.border
        self.column_2 = self.column_1 + self.plot_width + self.border
        self.column_3 = self.column_2 + self.plot_width + self.border * 2
        self.column_4 = self.column_3 + self.button_width + self.border

        self.button_row_1 = 1 - self.border - self.button_height
        self.button_row_2 = self.button_row_1 - self.border*2 - self.button_height
        self.button_row_3 = self.button_row_2 - self.border*2 - self.button_height
        self.button_row_4 = self.button_row_3 - self.border*2 - self.button_height
        self.button_row_5 = self.button_row_4 - self.border*2 - self.button_height
        self.button_row_6 = self.button_row_5 - self.border*2 - self.button_height

        self.controls_stop = self.column_2 - self.border/2 + self.controls_border/2
        self.controls_play = self.controls_stop - self.controls_border - self.controls_width
        self.controls_back = self.controls_play - self.controls_border - self.controls_width
        self.controls_next = self.controls_stop + self.controls_border + self.controls_width

        self.fig = plt.figure(figsize=(15, 5))
        self.scatter_axis = self.fig.add_axes([self.column_1, self.plot_y, self.plot_width, self.plot_height])
        self.graph_axis = self.fig.add_axes([self.column_2, self.plot_y, self.plot_width, self.plot_height])

        self.button_back_ax = self.fig.add_axes([self.controls_back, self.border, self.controls_width, self.controls_height])
        self.button_play_ax = self.fig.add_axes([self.controls_play, self.border, self.controls_width, self.controls_height])
        self.button_stop_ax = self.fig.add_axes([self.controls_stop, self.border, self.controls_width, self.controls_height])
        self.button_next_ax = self.fig.add_axes([self.controls_next, self.border, self.controls_width, self.controls_height])

        self.button_01_ax = self.fig.add_axes([self.column_3, self.button_row_1, self.button_width, self.button_height])
        self.button_02_ax = self.fig.add_axes([self.column_3, self.button_row_2, self.button_width, self.button_height])
        self.button_03_ax = self.fig.add_axes([self.column_3, self.button_row_3, self.button_width, self.button_height])
        self.button_04_ax = self.fig.add_axes([self.column_3, self.button_row_4, self.button_width, self.button_height])
        self.button_05_ax = self.fig.add_axes([self.column_3, self.button_row_5, self.button_width, self.button_height])
        self.button_06_ax = self.fig.add_axes([self.column_3, self.button_row_6, self.button_width, self.button_height])

        self.button_11_ax = self.fig.add_axes([self.column_4, self.button_row_1, self.button_width, self.button_height])
        self.button_12_ax = self.fig.add_axes([self.column_4, self.button_row_2, self.button_width, self.button_height])
        self.button_13_ax = self.fig.add_axes([self.column_4, self.button_row_3, self.button_width, self.button_height])
        self.button_14_ax = self.fig.add_axes([self.column_4, self.button_row_4, self.button_width, self.button_height])
        self.button_15_ax = self.fig.add_axes([self.column_4, self.button_row_5, self.button_width, self.button_height])
        self.button_16_ax = self.fig.add_axes([self.column_4, self.button_row_6, self.button_width, self.button_height])

        self.button_back = Button(self.button_back_ax, image=Icons.BACK, label="")
        self.button_play = Button(self.button_play_ax, image=Icons.PLAY, label="")
        self.button_stop = Button(self.button_stop_ax, image=Icons.STOP, label="")
        self.button_next = Button(self.button_next_ax, image=Icons.NEXT, label="")
        self.button_back_ax.axis("off")  # hide the border
        self.button_play_ax.axis("off")  # hide the border
        self.button_stop_ax.axis("off")  # hide the border
        self.button_next_ax.axis("off")  # hide the border

        self.button_01 = Slider(self.button_01_ax, "Sick ", 1, 10, 1, valstep=1)
        self.button_02 = Slider(self.button_02_ax, "Recovery ", 0.01, 0.8, 0.05)
        self.button_03 = Slider(self.button_03_ax, "Transmission ", 0.1, 1.0, 0.5)
        self.button_04 = Slider(self.button_04_ax, "Contact range ", 0.1, 10, 2, valstep=0.1)
        self.button_05 = Slider(self.button_05_ax, "Steps ", 10, 400, valstep=10)
        self.button_06 = Slider(self.button_06_ax, "Population ", 50, 1000, 50, valstep=50)

        self.button_11 = Slider(self.button_11_ax, "IMD ", 0.01, 1, 0.2)  # immunity decrease rate
        self.button_12 = Slider(self.button_12_ax, "RCI ", 0, 1, 0.5, )  # Recovered Immunity
        self.button_13 = Button(self.button_13_ax, "Empty")
        self.button_14 = Button(self.button_14_ax, "Empty")
        self.button_15 = Button(self.button_15_ax, "Empty")
        self.button_16 = Button(self.button_16_ax, "Generate New")


class Icons:
    PLAY = plt.imread("images/play.png")
    STOP = plt.imread("images/stop.png")
    BACK = plt.imread("images/back.png")
    NEXT = plt.imread("images/next.png")
