# Python Assignment: Premier League Player Analysis

This repository contains the code and resources for the "Analysis and Prediction of English Premier League Football Player Data" project.

## 📝 Description

This project aims to analyze a dataset of English Premier League (EPL) players to uncover insights and build predictive models. The primary objectives are:

* To perform exploratory data analysis (EDA) to understand the distribution and relationships of player attributes.
* To clean and preprocess the data for modeling.
* To build and evaluate machine learning models to predict a player's market value or performance metrics.
* To visualize the findings in a clear and informative way.

## 🚀 Getting Started

Follow these instructions to set up the project environment on your local machine.

### Prerequisites

Ensure you have the following software and libraries installed before you begin.

* [Python 3.8+](https://www.python.org/downloads/)
* [Jupyter Notebook](https://jupyter.org/install) or [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)
* Required Python packages are listed in `requirements.txt`.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/lightzgls/Python_Assignment.git](https://github.com/lightzgls/Python_Assignment.git)
    ```

2.  **Navigate to the project directory:**
    ```sh
    cd Python_Assignment
    ```

3.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Instructions on how to run the analysis and view the results.

* **To run the exploratory data analysis:**
    Open and run the cells in the Jupyter Notebook located in the `notebooks/` directory.
    ```sh
    jupyter notebook notebooks/data_analysis.ipynb
    ```

* **To run the main model training script:**
    ```sh
    python src/main.py
    ```

* **To run tests:**
    ```sh
    pytest
    ```

## 📂 Project Structure

A brief overview of the key files and directories in this project.

```
.
├── Report/
│   └── Assignment_Report.pdf
├── source code/
│   ├── Problem_I/
│   │   ├── Main.py
│   │   ├── README.md
│   │   └── uitils.py
│   ├── Problem_II/
│   │   ├── Part1.py
│   │   ├── Part2.py
│   │   ├── Part3(Player).py
│   │   ├── Part3(Team).py
│   │   └── Part4.py
│   ├── Problem_III/
│   │   ├── Find_optimal_k.py
│   │   ├── PCA_Graph.py
│   │   ├── PCA_plotly.py
│   │   └── heatmap.py
│   └── Problem_IV/
│       ├── Transfer_values.csv
│       ├── results.csv
│       ├── results2.csv
│       └── top_3.txt
├── README.md
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improving this project, please feel free to fork the repository and create a pull request. You can also open an issue with the "enhancement" tag.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/NewFeature`)
3.  Commit your Changes (`git commit -m 'Add some NewFeature'`)
4.  Push to the Branch (`git push origin feature/NewFeature`)
5.  Open a Pull Request

