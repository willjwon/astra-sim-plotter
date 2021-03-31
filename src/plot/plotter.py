"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List, Callable, Optional
from plot.plot_controller import PlotController
import pandas as pd
import numpy as np


class Plotter:
    def __init__(self, dataset: pd.DataFrame):
        """
        Instantiate a new Plotter instance.

        :param dataset: dataset to plot the graph.
        """
        self.dataset = dataset

    def plot(self, plot_over: List[str], grid_over: Optional[str],
             plot_fun: Callable, path: str, tight_axis: bool = False):
        """
        Plot plot_fun by iterating over plot_over configurations.
        Save the result pdf graphs into the path directory.

        :param plot_over: configurations to iterate over (split the graph).
                          for example, ['Workload', 'Passes', 'CommScale']
                          Will split workload, passes, and commscale
                          and plot them on separate figures.
        :param grid_over: if gridplot, set this to the column you want to use as a grid.
                          if not, set this to None.
        :param plot_fun: plotting function to use
        :param path: path to save result pdf plots
        """
        # set pre-aesthetics
        PlotController.set_pre_aesthetics()

        col_value = list()
        col_len = list()
        for col in plot_over:
            config = self.dataset[col].unique()
            col_value.append(config)
            col_len.append(len(config))

        # number of plots to draw
        plots_count = int(np.prod(col_len))

        # iterate over plots
        for plot_index in range(plots_count):
            # get col_index
            col_index = []

            numerator = plot_index
            denominator = plots_count
            for l in col_len:
                denominator = denominator // l
                col_index.append(numerator // denominator)
                numerator %= denominator

            # refine dataset
            data = self.dataset.loc[self.dataset[plot_over[0]] == col_value[0][col_index[0]]]
            for i in range(1, len(col_index)):
                data = data.loc[data[plot_over[i]] == col_value[i][col_index[i]]]

            # check data validity
            if len(data) <= 0:
                continue

            # print log message
            running_configs = list()
            print(f"Plotting [{plot_fun.__name__}] on [", end="")
            for i in range(len(col_index) - 1):
                print(f"{plot_over[i]}: {col_value[i][col_index[i]]}, ", end="")
            print(f"{plot_over[-1]}: {col_value[-1][col_index[-1]]}].")

            # draw plot
            plot_fun(dataset=data, plot_over=plot_over, grid_over=grid_over,
                     path=path, tight_axis=tight_axis)
