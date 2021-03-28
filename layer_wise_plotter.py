"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from csv_loader import CSVLoader
from breakdown_plot_drawer import *
from grid_plot_drawer import *


def main():
    # reset and make graph result directory
    if not os.path.exists('./graph'):
        os.makedirs('./graph')

    # load dataset
    csv_loader = CSVLoader(dir='./')
    dataset = csv_loader.load_dataset(data_type='layer_wise')

    # draw stacked bar plot
    print("Layerwise Plotter")
    for workload in dataset['Workload'].unique():
        for comm_scale in dataset['CommScale'].unique():
            for passes in dataset['Passes'].unique():
                # filter data
                data = dataset.loc[dataset['Workload'] == workload]
                data = data.loc[data['CommScale'] == comm_scale]
                data = data.loc[data['Passes'] == passes]
                if len(data) <= 0:
                    continue

                print(f"Drawing Workload: {workload}, Comm-scale: {comm_scale}, Passes: {passes}")

                # draw non-normalized figure
                draw_layer_wise_average_chunk_latency_grid(dataset=data,
                                                      dir='./graph',
                                                      workload=workload,
                                                      comm_scale=comm_scale,
                                                      passes=passes,
                                                      normalize=False)

                # draw normalized plot
                draw_layer_wise_average_chunk_latency_grid(dataset=data,
                                                      dir='./graph',
                                                      workload=workload,
                                                      comm_scale=comm_scale,
                                                      passes=passes,
                                                      normalize=True)

                # draw non-normalized figure
                draw_layer_wise_average_chunk_latency(dataset=data,
                                                      dir='./graph',
                                                      workload=workload,
                                                      comm_scale=comm_scale,
                                                      passes=passes,
                                                      normalize=False)

                # draw normalized plot
                draw_layer_wise_average_chunk_latency(dataset=data,
                                                      dir='./graph',
                                                      workload=workload,
                                                      comm_scale=comm_scale,
                                                      passes=passes,
                                                      normalize=True)


if __name__ == '__main__':
    main()
