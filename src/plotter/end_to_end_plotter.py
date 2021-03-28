"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os
from ..data.csv_loader import CSVLoader
from breakdown_plot_drawer import *
from grid_plot_drawer import *
from ..data.topology_config_parser import TopologyConfigParser
from ..data.system_config_parser import SystemConfigParser


def main():
    # reset and make graph result directory
    if not os.path.exists('../../graph'):
        os.makedirs('../../graph')

    # parsers
    network_parser = TopologyConfigParser(dir='../inputs/network/analytical')
    system_parser = SystemConfigParser(dir='../inputs/system')

    # load dataset
    print("<Reading Dataset>")

    csv_loader = CSVLoader(network_parser=network_parser, system_parser=system_parser, dir='../../')
    dataset = csv_loader.load_dataset(data_type='end_to_end')
    # print(dataset.to_string())
    # exit(-1)

    # setup
    draw_breakdown_plot_input = input("Draw breakdown plot? (y / N): ")
    cut_plot_input = input("Draw cut plot? (y / N): ")

    draw_breakdown_plot = False
    if draw_breakdown_plot_input.lower() == 'y':
        draw_breakdown_plot = True
    draw_cut_plot = False
    if cut_plot_input.lower() == 'y':
        draw_cut_plot = True
    print(draw_breakdown_plot, draw_cut_plot)

    # draw graphs
    print("<End to End Plotter>")
    for workload in dataset['Workload'].unique():
        for comm_scale in dataset['CommScale'].unique():
            for passes in dataset['Passes'].unique():
                # filter dataset
                data = dataset.loc[dataset['Workload'] == workload]
                data = data.loc[data['CommScale'] == comm_scale]
                data = data.loc[data['Passes'] == passes]
                if len(data) <= 0:
                    continue

                print(f"(Barplot) Drawing Workload: {workload}, CommScale: {comm_scale}, Passes: {passes}")

                # draw plots
                draw_running_time_barplot_grid(dataset=data, dir='../../graph',
                                               workload=workload, comm_scale=comm_scale, passes=passes, cut_min=False)
                draw_running_time_cost_scatter_plot(dataset=data, dir='../../graph',
                                                    workload=workload, comm_scale=comm_scale, passes=passes)

                if draw_cut_plot:
                    draw_running_time_barplot_grid(dataset=data, dir='../../graph',
                                                   workload=workload, comm_scale=comm_scale, passes=passes,
                                                   cut_min=True)

                if draw_breakdown_plot:
                    draw_running_time_barplot(dataset=data, dir='../../graph',
                                              workload=workload, comm_scale=comm_scale, passes=passes, cut_min=False)

                if draw_breakdown_plot and draw_cut_plot:
                    draw_running_time_barplot(dataset=data, dir='../../graph',
                                              workload=workload, comm_scale=comm_scale, passes=passes, cut_min=True)

    for workload in dataset['Workload'].unique():
        for topology in dataset['PhysicalTopology'].unique():
            for passes in dataset['Passes'].unique():
                # filter dataset
                data = dataset.loc[dataset['Workload'] == workload]
                data = data.loc[data['PhysicalTopology'] == topology]
                data = data.loc[data['Passes'] == passes]
                if len(data) <= 0:
                    continue

                print(f"(CommScale) Drawing Workload: {workload}, Topology: {topology}, Passes: {passes}")
                # draw plots
                draw_runtime_commscale_lineplot(dataset=data, dir='../../graph',
                                                workload=workload, topology=topology, passes=passes, cut_min=False)
                draw_bw_latency_commscale_lineplot(dataset=data, dir='../../graph',
                                                   workload=workload, topology=topology, passes=passes, cut_min=False)
                draw_bw_utilization_dim_commscale_lineplot(dataset=data, dir='../../graph',
                                                           workload=workload, topology=topology, passes=passes,
                                                           cut_min=False)

                if draw_cut_plot:
                    draw_runtime_commscale_lineplot(dataset=data, dir='../../graph',
                                                    workload=workload, topology=topology, passes=passes, cut_min=True)
                    draw_bw_latency_commscale_lineplot(dataset=data, dir='../../graph',
                                                       workload=workload, topology=topology, passes=passes,
                                                       cut_min=True)
                    draw_bw_utilization_dim_commscale_lineplot(dataset=data, dir='../../graph',
                                                               workload=workload, topology=topology, passes=passes,
                                                               cut_min=True)


if __name__ == '__main__':
    main()
