import os
import string
import random

import pandas as pd
import numpy as np


def generate_random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string of a specified length.

    Args:
        length (int): The length of the string to generate. Defaults to 8.

    Returns:
        str: A randomly generated alphanumeric string.
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=length))


def generate_dataset(data_path: str, seed: int = 42, num_rows: int = 1000000) -> None:
    """Generate a dataset containing random string, numeric, and categorical data,
    with a specified proportion of missing values, and save it as a CSV file.

    Args:
        data_path (str): The file path where the dataset will be saved.
        seed (int): The seed for random number generation to ensure reproducibility.
            Defaults to 42.
        num_rows (int): The number of rows in the dataset. Defaults to 100,000.
    """
    # Ensure the directory exists; create it if it doesn't
    dir_path = os.path.dirname(data_path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Set the random seed for reproducibility
    np.random.seed(seed)
    random.seed(seed)

    # Generate string data: a list of random alphanumeric strings
    string_data = [generate_random_string(10) for _ in range(num_rows)]

    # Generate numeric data: random numbers from a normal distribution
    numeric_data = np.random.normal(0, 100, num_rows)

    # Generate categorical data: random selection from specified categories
    category_data = np.random.choice(["a", "b", "c", "d", "e"], num_rows)

    # Create a DataFrame with the generated data
    df = pd.DataFrame({
        'string_val': string_data,
        'numeric_val': numeric_data,
        'category_val': category_data
    })

    # Define the proportion of missing values
    missing_rate = 0.01  # 1% missing values
    num_missing = int(num_rows * missing_rate)

    # Introduce missing values randomly in each column
    for column in df.columns:
        missing_indices = np.random.choice(df.index, num_missing, replace=False)
        df.loc[missing_indices, column] = np.nan

    # Save the DataFrame to a CSV file at the specified path
    df.to_csv(data_path, index=False)
