# ASTRA-sim-plotter
## Setup
1. Paste the `inputs/` directory from ASTRA-sim. This directory should include:
- `inputs/network/analytical/`
- `inputs/system/`
2. Paste the `result/` directory made by ASTRA-sim (analytical backend) run script.

## Draw
- To draw plots, run `src/draw.py`.
```bash
python3 src/draw.py
```

- To draw activity-time plots of each dimension, run `src/draw_activity_plot.py`.
```bash
python3 src/draw_activity_plot.py
```
