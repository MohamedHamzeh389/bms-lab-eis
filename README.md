# bms-lab-eis

Battery EIS / Warburg impedance RC-ladder approximation project.

## Layout

```
notebooks/    Jupyter notebooks
  Warburg_simulation.ipynb   main analysis: RC-ladder fit, model order
                              selection, time-domain integrator comparison
  battery_simulation.ipynb   battery time-domain simulation notebook

scripts/      Standalone Python scripts
  eis_fit.py                Randles+CPE+Warburg fit against real EIS data
                              (run from the repository root: `python scripts/eis_fit.py`)

data/         Input data files
  SampleEISData.mat

figures/      Generated plots (PDF + PNG), exported from notebooks/scripts

paper/        LaTeX paper
  warburg_paper.tex
  warburg_paper.pdf
```
