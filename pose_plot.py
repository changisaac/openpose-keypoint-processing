# Author: Isaac Chang
# Contact: chang.isaac@outlook.com
# Date: 03/16/2021

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class PosePlot:
    """
    This class contains functions for animating the plot of angles between joints
    extracted from OpenPose.
    """

    def __init__(self, angles, frame_length, title, ylabel, xlabel):
        # Lis of angles to plot
        self._angles = angles
        # Frame length of animation window
        self._frame_length = frame_length
        # Title of plot
        self._title = title
        # Title of y-axis
        self._ylabel = ylabel
        # Title of x-axis
        self._xlabel = xlabel

        self._left_frame = 0
        self._right_frame = 0
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)
        self._animation = None

    def _update(self, i):
        plot_angles = self._angles[self._left_frame:self._right_frame]
        plot_frame_nums = range(self._left_frame, self._right_frame)

        self._ax.clear()
        self._ax.plot(plot_frame_nums, plot_angles)

        self._fig.set_facecolor("grey")
        self._ax.set_facecolor("black")
        self._ax.set_ylim([-10, 200])

        plt.title(self._title)
        plt.ylabel(self._ylabel)
        plt.xlabel(self._xlabel)

        self._right_frame = (self._right_frame + 1) % len(self._angles)

        if self._right_frame < self._frame_length:
            self._ax.set_xlim([0, self._frame_length])
        else:
            self._left_frame = (self._left_frame + 1) % len(self._angles)

        if self._right_frame == len(self._angles):
            self._animation.event_source.stop()

    def animate(self, save_file_name=None, fps=30):
        """
        Animate the plot to display the angles per frame. Includes options to
        save the animation as a video file and specify frame rate. If a file name
        is not provided then the animated plot will simply be displayed in a window.
        """

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
        frame_interval = (1.0 / fps) * 1000.0 

        print("Generating plot animation")

        self._animation = animation.FuncAnimation(self._fig, self._update,
                                                  interval=frame_interval,
                                                  save_count=len(self._angles))
        if save_file_name:
            self._animation.save(save_file_name, writer=writer)
            print("Plot animation has been saved at " + save_file_name)
        else:
            plt.show()
