import time
from typing import Callable
import statistics

import pandas as pd
import polars as pl


class PandasPolarsComparator:
    """Compares performance between pandas and polars for data operations."""

    def __init__(self, data_path: str) -> None:
        """
        Initializes the comparator with the path to the data file.

        Args:
            data_path: Path to the CSV data file.
        """
        self.data_path = data_path

    def _measure_time(
            self, func: Callable[[], pd.DataFrame | pl.DataFrame], library_type: str
        ) -> tuple[pd.DataFrame | pl.DataFrame, dict[str, float]]:
        """
        Measures the execution time of a function over multiple iterations.

        Args:
            func: A callable that returns a DataFrame when executed.
            library_type: A string indicating the library used ('pandas' or 'polars').

        Returns:
            A tuple containing the DataFrame result from the function and a dictionary
            with the library name as the key and the average execution time as the value.
        """
        elapsed_times = []

        # Execute the function 10 times to gather execution times
        for _ in range(10):
            start_time = time.time()
            df = func()
            elapsed_time = time.time() - start_time
            elapsed_times.append(elapsed_time)

        # Calculate the average execution time
        average_time = statistics.mean(elapsed_times)
        result = {library_type: average_time}
        return df, result

    def compare(self) -> dict[str, dict[str, float]]:
        """
        Compares the performance of pandas and polars.

        Returns:
            A dictionary with operation types as keys and dictionaries as values.
            Each inner dictionary contains the library names as keys and their
            corresponding average execution times as values.
        """
        results = {}

        # Measure csv loading time
        pd_df, pd_read_time = self._measure_time(
            lambda: pd.read_csv(self.data_path), "pandas")
        pl_df, pl_read_time = self._measure_time(
            lambda: pl.read_csv(self.data_path), "polars")
        
        # Measure filter processing time
        _, pd_filter_time = self._measure_time(
            lambda: pd_df[pd_df['numeric_val'] > 20.0], "pandas")
        _, pl_filter_time = self._measure_time(
            lambda: pl_df.filter(pl.col('numeric_val') > 20.0), "polars")

        # Add times into results dictionary
        results.update({
            "read": pd_read_time | pl_read_time,
            "filter": pd_filter_time | pl_filter_time,
        })
        return results
