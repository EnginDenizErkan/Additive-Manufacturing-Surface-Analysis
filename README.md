# Additive Manufacturing Surface Analysis

<p align="center">
  <b>Data-driven surface roughness analysis for additive manufacturing</b><br/>
  Interactive web application and reproducible analysis assets
</p>

## Overview

This repository contains the code and analysis assets developed for data-driven surface roughness prediction in additive manufacturing. It includes:

- an interactive web application for visualization and exploration,
- a reproducible notebook-based analysis workflow,
- the dataset required to reproduce the main computational results reported in the manuscript.

## Live Website

A live version of the web application is available at:

**https://additive-manufacturing-surface-analysis.onrender.com/**

Please note that the application may occasionally take a few seconds to open. In such cases, please wait briefly for the server to respond.

## Repository Structure

- `app/`: Source code for the web application
- `Data_Analysis/`: Notebooks used for the computational analysis
- `dataset/`: Used Dataset
- `requirements.txt`: Python dependencies for the web application
- `environment.yml`: Conda environment file for reproducible notebook execution

## Data Analysis Assets

The `Data_Analysis/` folder contains the files required to reproduce the computational analysis reported in the manuscript:

- `Data_Analysis/Surface_Roughness_Prediction.ipynb`: main notebook containing the analysis, model training, and prediction workflow
- `Data_Analysis/mahr_data.csv`: dataset used in the notebook

## Reproducibility and Environment Setup

This repository provides the code and workflow used to reproduce the results reported in the manuscript. The notebook-based analysis is included to support transparent and structured reproduction of the computational experiments, model training procedure, and reported outputs.

### Environment Setup

To reproduce the notebook results, first create a Conda environment using the provided `environment.yml` file.

On **Windows**, use **Anaconda Prompt**.  
On **Linux** or **macOS**, use a **Terminal**.

#### View available Conda environments

```bash
conda env list
```

#### Create the environment

```bash
conda env create -f environment.yml
```

If needed, the full file path may also be used:

```bash
conda env create -f C:\Users\User\Desktop\Additive-Manufacturing-Surface-Analysis\environment.yml
```

#### Activate the environment

```bash
conda activate surface_roughness_env
```

## Running the Web Application Locally

After activating the environment, the web application can be launched locally.

### macOS / Linux

```bash
uvicorn app.main:app --reload --port 8000
```

### Windows

```bash
python -m uvicorn app.main:app --reload --port 8000
```

After the server starts, open the following address in a browser:

```text
http://localhost:8000
```

## Running the Notebooks

After activating the environment, launch Jupyter Notebook or JupyterLab and open the notebooks in the `Data_Analysis/` folder.

### `Data_Analysis/Exploratory_Data_Analysis.ipynb`
This notebook contains the exploratory data analysis of the experimental dataset, including descriptive statistics and visual examination of the relationships between surface roughness and key process variables.

### `Data_Analysis/MLP_Real_Data_Only.ipynb`
This notebook contains the machine learning workflow based only on the experimental dataset. It includes preprocessing, model development, and evaluation of the MLP model trained exclusively on real data.

### `Data_Analysis/MLP_Real_And_Synthetic_Data.ipynb`
This notebook contains the machine learning workflow using the combined experimental and synthetic dataset. It is provided to examine the effect of synthetic data augmentation on model training and predictive performance.

For full reproducibility, it is recommended to restart the kernel and run all cells sequentially from the beginning.

## Notes

- Use the notebooks in `Data_Analysis/` to reproduce and extend the computational analysis.
- Use the locally launched or deployed web application for interactive exploration.
- The deployed application is intended for demonstration and visualization, while the notebooks in `Data_Analysis/` provides the main reproducible analysis workflow.