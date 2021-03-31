"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List, Optional
import pandas as pd
import seaborn as sns
from plot.plot_controller import PlotController


def commstimebwdim_commscale(dataset: pd.DataFrame, plot_over: List[str], grid_over: Optional[str], path: str, tight_axis: bool = False):
    """
    <Lineplot> CommsTime_BW_dim - CommScale

    :param dataset: dataset to use
    :param plot_over: column names to iterate over when drawing.
                      used for deciding figure title / filename etc.
    :param path: path to save graph
    :param tight_axis: if true, tightly cut y-axis range.
                       if false, y-axis starts with 0.
    """
    # melt dataset
    dimensions_to_melt = list(filter(lambda x: x.startswith('CommsTime_BW_Dim'), dataset.columns))
    dimensions_to_melt.insert(0, 'CommsTime_BW')

    melt_data = pd.melt(dataset, id_vars=['CommScale'], value_vars=dimensions_to_melt,
                        var_name='Dimension', value_name='CommsTime_BW_Dim')
    melt_data.dropna(inplace=True)
    for index, row in melt_data.iterrows():
        if row['Dimension'] == 'CommsTime_BW':
            melt_data.loc[index, 'Dimension'] = 'Total'
        else:
            melt_data.loc[index, 'Dimension'] = row['Dimension'].split('_')[2]

    # create plot_controller
    plot_controller = PlotController(dataset=dataset, melt_data=melt_data,
                                     plot_over=plot_over, ncols=1)

    # aesthetics pre-update
    plot_controller.set_pre_aesthetics()

    # draw plot
    ax = plot_controller.get_axes()
    sns.lineplot(data=melt_data,
                 x='CommScale', y='CommsTime_BW_Dim',
                 style='Dimension', hue='Dimension',
                 markers=True, dashes=False, markersize=15,
                 ax=ax)

    # aesthetics update
    plot_controller.set_xlabel(xlabel='CommScale (MB)')
    plot_controller.set_ylabel(ylabel='CommsTime_BW_Dim')
    plot_controller.set_title()
    plot_controller.adjust_y_axis_range(yname='CommsTime_BW_Dim', tight_axis=tight_axis)
    plot_controller.set_post_aesthetics()

    # save plot
    plot_controller.save(path=path)
    # plot_controller.show()
