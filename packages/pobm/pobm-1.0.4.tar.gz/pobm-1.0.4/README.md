# PhysioZoo OBM documentation

Oximetry digital biomarkers for the analysis of continuous oximetry (SpO2) time series.

Based on the paper Levy Jeremy, Álvarez Daniel, Rosenberg Aviv A., del Campo Felix and Behar Joachim A. "Oximetry digital biomarkers for assessing respiratory function during sleep: standards of measurement, physiological interpretation, and clinical use". 
Accepted for publication in NPJ Digital Medicine.

## Description

Five types of biomarkers may be evaluated:

1.  General statistics: time-based statistics describing the oxygen saturation time series data distribution.

2.  Complexity: quantify the presence of long-range correlations in non-stationary time series.

3.  Periodicity: quantify consecutive events creating some periodicity in the oxygen saturation time series.

4.  Desaturations: time-based measures that are descriptive statistics of the desaturation patterns happening throughout the time series.

5.  Hypoxic burden: time-based measures quantifying the overall degree of hypoxemia imposed to the heart and other organs during the recording period.

## Installation

Available on pip, with the command: 
pip install pobm

pip project: https://pypi.org/project/pobm/

## Requirements

numpy==1.18.2

scikit-learn==0.22.2

scipy==1.4.1

lempel-ziv-complexity==0.2.2

All the requirements are installed when the toolbox is installed, no need for additional commands.

## Documentation

Available at https://oximetry-toolbox.readthedocs.io/en/latest/
