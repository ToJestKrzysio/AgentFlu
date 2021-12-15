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

        # self.button_back_ax.axis("off") # should hide the border
        self.button_back = Button(self.button_back_ax, image=Icons.BACK, label="")
        self.button_play = Button(self.button_play_ax, image=Icons.PLAY, label="")
        self.button_stop = Button(self.button_stop_ax, image=Icons.STOP, label="")
        self.button_next = Button(self.button_next_ax, image=Icons.NEXT, label="")

        self.button_01 = TextBox(self.button_01_ax, "")
        self.button_02 = TextBox(self.button_02_ax, "")
        self.button_03 = TextBox(self.button_03_ax, "")
        self.button_04 = TextBox(self.button_04_ax, "")
        self.button_05 = TextBox(self.button_05_ax, "")
        self.button_06 = TextBox(self.button_06_ax, "")

        self.button_11 = Button(self.button_11_ax, "")
        self.button_12 = Button(self.button_12_ax, "")
        self.button_13 = Button(self.button_13_ax, "")
        self.button_14 = Slider(self.button_14_ax, "", 0, 10, 1)
        self.button_15 = Slider(self.button_15_ax, "", 0, 10, 1)
        self.button_16 = Slider(self.button_16_ax, "", 0, 10, 1)


class Icons:
    PLAY = plt.imread("images/play.png")
    STOP = plt.imread("images/stop.png")
    BACK = plt.imread("images/back.png")
    NEXT = plt.imread("images/next.png")
