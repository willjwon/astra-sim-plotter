"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List, Optional
import pandas as pd
import seaborn as sns
from plot.plot_controller import PlotController


def commstime_topology(dataset: pd.DataFrame, plot_over: List[str], grid_over: Optional[str],
                       path: str, tight_axis: bool = False):
    """
    <Barplot> CommsTime - Topology

    :param dataset: dataset to use
    :param plot_over: column names to iterate over when drawing.
                  used for deciding figure title / filename etc.
    :param grid_over: set this if gridplot.
                      if not, set this to None.
    :param path: path to save graph
    :param tight_axis: if true, tightly cut y-axis range.
                       if false, y-axis starts with 0.
    """
    if grid_over is None:
        grid_values = None
        plot_controller = PlotController(dataset=dataset, melt_data=None, plot_over=plot_over, ncols=1,
                                         width=7, height=15)
    else:
        grid_values = dataset[grid_over].unique()

        # if unique grid_value, skip the gridplot
        if len(grid_values) <= 1:
            return

        # if not, create gridplot
        plot_controller = PlotController(dataset=dataset, melt_data=None, plot_over=plot_over, ncols=len(grid_values),
                                         width=5, height=15)

    # aesthetics pre-update
    plot_controller.set_pre_aesthetics()

    # draw plot
    if grid_over is None:
        ax = plot_controller.get_axes()
        sns.barplot(data=dataset,
                    x='Topology', y='CommsTime',
                    hue='Topology',
                    ax=ax,
                    dodge=False)
    else:
        axes = plot_controller.get_axes()
        for i in range(len(grid_values)):
            ax = axes[i]
            grid_value = grid_values[i]

            data = dataset.loc[dataset[grid_over] == grid_value]
            sns.barplot(data=data,
                        x='Topology', y='CommsTime',
                        hue='Topology',
                        ax=ax,
                        dodge=False)

            ax.set_title(f"{grid_value}")

    # todo: add theoretical optimal point
    # sns.lineplot(data=dataset,
    #              x='Topology', y='CommsTime_Optimal',
    #              ax=ax)

    # aesthetics update
    plot_controller.set_xlabel(xlabel='Topology')
    plot_controller.rotate_xlabel()
    plot_controller.set_ylabel(ylabel='CommsTime (ms)')
    plot_controller.set_title()
    plot_controller.adjust_y_axis_range(yname='CommsTime', tight_axis=tight_axis)
    plot_controller.set_post_aesthetics(remove_legend=True)

    # save plot
    plot_controller.save(path=path)
    # plot_controller.show()
