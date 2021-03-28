"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


class PlotController:
    """
    Class with common plotter helper methods.
    Used to create/design/control plots.
    """

    def __init__(self, dataset: pd.DataFrame, ncols=1):
        """
        Instantiate a new PlotController object.
        Create (1, ncols) number of plots.

        :param dataset: dataset to use
        :param ncols: columns count in a plot
        """
        self.ncols = ncols
        self.dataset = dataset

        # create fig and axes
        self.fig, self.axes = plt.subplots(nrows=1, ncols=ncols)

        # self.axes always in ndarray form
        if self.ncols == 1:
            self.axes = np.array([self.axes])

        # flatten the axes
        self.axes = self.axes.flatten()

    @staticmethod
    def set_pre_aesthetics():
        """
        Set seaborn plot pre-aesthetics.
        """
        # aesthetics pre-update
        sns.set(font_scale=1.5)
        sns.set_style('ticks')

    def set_post_aesthetics(self, remove_legend: bool = False):
        """
        Set seaborn plot post-aesthetics.

        :param remove_legend: if True, legend will be removed from the reslting plot.
        """
        if remove_legend:
            for ax in self.axes:
                ax.get_legend().remove()

        fig_width = 10
        fig_height = 7 * self.ncols
        self.fig.set_size_inches((fig_width, fig_height))

    def get_axes(self):
        """
        :return: Axes instance if number of axes is 1, ndarray(Axes) if there're multiple axes.
        """
        if self.ncols == 1:
            return self.axes[0]  # return flat ax

        return self.axes

    def adjust_y_axis_range(self, yname: str, tight_axis: bool = False):
        """
        Adjust (scale) y axis range.

        :param yname: y axis value name (used to retrieve min/max value from the dataset)
        :param tight_axis: if True, y axis will be tightly adjusted.
                           if False, y axis will start from 0.
        """
        y_min = min(self.dataset[yname])
        y_max = max(self.dataset[yname])

        # if y_min = y_max, only one bar.
        #   dist = y_max
        # if y_min != y_max, multiple bars.
        #   dist = y_max - y_min
        dist = y_max
        if y_min < y_max:  # if y_min != y_max
            dist -= y_min

        margin = 0.1 * dist
        ylim_min = 0
        ylim_max = y_max + margin
        if tight_axis:
            ylim_min = y_min - margin

        for ax in self.axes:
            ax.set_ylim(ylim_min, ylim_max)

    def parse_dataset(self):
        """
        Parse dataset to retrieve meaningful data,
        which can be used to generate filename, plot title, etc.

        :return: dictionary with parsed results
        """
        parsing_result = dict()
        datapoint = self.dataset.iloc[0]

        parsing_result['RunName'] = datapoint['RunName']
        parsing_result['Passes'] = datapoint['Passes']
        parsing_result['Workload'] = datapoint['Workload']

        return parsing_result

    def set_title(self):
        """
        Add a title to the plot.
        """
        config = self.parse_dataset()
        title = f"{config['Workload']} ({config['RunName']})\n" \
                f"(Passes: {config['Passes']})"

        self.fig.suptitle(title)

    def show(self):
        """
        Show the plot using the matplotlib library.
        """
        self.fig.tight_layout()
        plt.show()
        self.fig.clf()
        plt.close(fig=self.fig)

    def save(self, path: str):
        """
        Save the plot as a pdf file

        :param path: path to save the plot.
        """
        config = self.parse_dataset()

        # subdirectory_path = os.path.join(subdirectory_path, config['Workload'], config['RunName'])
        dir_path = os.path.join(path, config['Workload'])
        assert os.path.exists(dir_path), f"Path {dir_path} doesn't exist."

        filename = f"{config['Workload']}_{config['RunName']}_{config['Passes']}pass.pdf"
        file_path = os.path.join(dir_path, filename)

        self.fig.tight_layout()
        self.fig.savefig(file_path)
        self.fig.clf()
        plt.close(fig=self.fig)
