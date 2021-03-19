#!/bin/zsh
set -e

python3 end_to_end_plotter.py
python3 layer_wise_plotter.py
