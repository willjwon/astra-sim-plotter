"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from src.data.dataset_type import DatasetType
from src.data.dataset_loader import DatasetLoader
from src.plot.plot_controller import PlotController
from src.plot.commstime_commscale import commstime_commscale
from src.plot.commstimebw_commscale import commstimebw_commscale
from src.plot.commstimebwdim_commscale import commstimebwdim_commscale
from src.plot.commstimechunk_topology import commstimechunk_topology
from src.plot.commstime_topology import commstime_topology
from src.plot.commstime_cost import commstime_cost
from src.helper.directory_manager import DirectoryManager
from src.plot.plotter import Plotter


def main():
    # Run plot pre_aesthetics
    PlotController.set_pre_aesthetics()

    # load dataset
    dataset_loader = DatasetLoader(csv_dir='../result/',
                                   system_dir='../inputs/system',
                                   topology_dir='../inputs/network/analytical')
    backend_end_to_end_dataset = dataset_loader.load_dataset(dataset_type=DatasetType.BackendEndToEnd)
    backend_layerwise_dataset = dataset_loader.load_dataset(dataset_type=DatasetType.BackendLayerWise)

    # prepare plotter
    end_to_end_plotter = Plotter(dataset=backend_end_to_end_dataset)
    layerwise_plotter = Plotter(dataset=backend_layerwise_dataset)

    # create top directory and subdirectories
    directory_manager = DirectoryManager(top_directory='../graph')
    directory_manager.create_top_directory(reset_if_exist=False)
    for workload in backend_end_to_end_dataset['Workload'].unique():
        # grid directories
        directory_manager.create_subdirectory(path=f'CommsTime_CommScale/{workload}', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTime_Topology/{workload}', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTime_Cost/{workload}', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTimeBW_CommScale/{workload}', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTimeBwDim_CommScale/{workload}', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTimeChunk_Topology/{workload}', reset_if_exist=True)

        # breakdown directories
        directory_manager.create_subdirectory(path=f'CommsTime_CommScale/{workload}/breakdown', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTime_Topology/{workload}/breakdown', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTime_Cost/{workload}/breakdown', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTimeBW_CommScale/{workload}/breakdown', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTimeBwDim_CommScale/{workload}/breakdown', reset_if_exist=True)
        directory_manager.create_subdirectory(path=f'CommsTimeChunk_Topology/{workload}/breakdown', reset_if_exist=True)

    # plot required figures
    # grid plots
    end_to_end_plotter.plot(plot_over=['Passes', 'Workload', 'CommScale'],
                            grid_over='RunName',
                            plot_fun=commstime_topology,
                            path='../graph/CommsTime_Topology')
    layerwise_plotter.plot(plot_over=['Passes', 'Workload', 'CommScale'],
                            grid_over='RunName',
                            plot_fun=commstimechunk_topology,
                            path='../graph/CommsTimeChunk_Topology')

    # breakdown plots
    end_to_end_plotter.plot(plot_over=['RunName', 'Passes', 'Workload'],
                            grid_over=None,
                            plot_fun=commstime_commscale,
                            path='../graph/CommsTime_CommScale')
    end_to_end_plotter.plot(plot_over=['RunName', 'Passes', 'Workload', 'CommScale'],
                            grid_over=None,
                            plot_fun=commstime_topology,
                            path='../graph/CommsTime_Topology')
    end_to_end_plotter.plot(plot_over=['Passes', 'Workload', 'CommScale'],
                            grid_over=None,
                            plot_fun=commstime_cost,
                            path='../graph/CommsTime_Cost')
    end_to_end_plotter.plot(plot_over=['RunName', 'Passes', 'Workload'],
                            grid_over=None,
                            plot_fun=commstimebw_commscale,
                            path='../graph/CommsTimeBW_CommScale',
                            tight_axis=True)
    end_to_end_plotter.plot(plot_over=['RunName', 'Passes', 'Workload', 'PhysicalTopology'],
                            plot_fun=commstimebwdim_commscale,
                            grid_over=None,
                            path='../graph/CommsTimeBwDim_CommScale',
                            tight_axis=True)
    layerwise_plotter.plot(plot_over=['RunName', 'Passes', 'Workload', 'CommScale'],
                           grid_over=None,
                           plot_fun=commstimechunk_topology,
                           path='../graph/CommsTimeChunk_Topology',
                           tight_axis=True)


if __name__ == '__main__':
    main()
