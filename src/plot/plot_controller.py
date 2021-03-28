"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List
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

    def __init__(self, dataset: pd.DataFrame, plot_over: List[str], ncols: int =1):
        """
        Instantiate a new PlotController object.
        Create (1, ncols) number of plots.

        :param dataset: dataset to use
        :param ncols: columns count in a plot
        """
        self.ncols = ncols
        self.plot_over = plot_over
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
        else:
            for ax in self.axes:
                ax.legend(loc="center left", bbox_to_anchor=(1.04, 0.5))

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

    def adjust_x_axis_range(self, xname: str, tight_axis: bool = False):
        """
        Adjust (scale) y axis range.

        :param xname: y axis value name (used to retrieve min/max value from the dataset)
        :param tight_axis: if True, y axis will be tightly adjusted.
                           if False, y axis will start from 0.
        """
        x_min = min(self.dataset[xname])
        x_max = max(self.dataset[xname])

        # if x_min = x_max, only one bar.
        #   dist = x_max
        # if x_min != x_max, multiple bars.
        #   dist = x_max - x_min
        dist = x_max
        if x_min < x_max:  # if x_min != x_max
            dist -= x_min

        margin = 0.1 * dist
        xlim_min = 0
        xlim_max = x_max + margin
        if tight_axis:
            xlim_min = x_min - margin

        for ax in self.axes:
            ax.set_xlim(xlim_min, xlim_max)

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

    def set_xlabel(self, xlabel: str):
        """
        Set xlabel (x axis name) of the plot.

        :param xlabel: new xlabel name to set.
        """
        for ax in self.axes:
            ax.set_xlabel(xlabel)

    def set_ylabel(self, ylabel: str):
        """
        Set ylabel (axis name) of the plot.

        :param ylabel: new ylabel name to set
        """
        # todo: update this
        for ax in self.axes:
            ax.set_ylabel(ylabel)

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
        parsing_result['CommScale'] = datapoint['CommScale']

        return parsing_result

    def set_title(self):
        """
        Add a title to the plot.
        """
        config = self.parse_dataset()

        # populate title string
        title = ""

        if 'Workload' in self.plot_over:
            title += config['Workload']
        if 'RunName' in self.plot_over:
            title += f" ({config['RunName']})"
        if 'CommScale' in self.plot_over:
            title += f"\nCommScale: {config['CommScale']} MB"
        if 'Passes' in self.plot_over:
            title += f"\nPass: {config['Passes']}"

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

        filename = self.create_plot_filename()
        file_path = os.path.join(dir_path, filename)

        self.fig.tight_layout()
        self.fig.savefig(file_path)
        self.fig.clf()
        plt.close(fig=self.fig)

    def create_plot_filename(self):
        """
        Create plot pdf filename, based on plot_over configurations.

        :return: filename to use
        """
        config = self.parse_dataset()
        filename_str = list()

        if 'Workload' in self.plot_over:
            filename_str.append(config['Workload'])
        if 'RunName' in self.plot_over:
            filename_str.append(config['RunName'])
        if 'CommScale' in self.plot_over:
            filename_str.append(f"{config['CommScale']}mb")
        if 'Passes' in self.plot_over:
            filename_str.append(f"{config['Passes']}pass")

        filename = "_".join(filename_str)
        return filename + ".pdf"
