import os
import time
from typing import Callable
import statistics

import pandas as pd
import polars as pl
from rich.console import Console


class PandasPolarsComparator:
    """Compares performance between pandas and polars for data operations."""

    def __init__(self, data_path: str, console: Console) -> None:
        """
        Initializes the comparator with the path to the data file.

        Args:
            data_path: Path to the CSV data file.
        """
        self.data_path = data_path
        self.console = console

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


        # Measure processing time for loading csv
        pd_df, pd_load_time = self._measure_time(
            lambda: pd.read_csv(self.data_path), "pandas")
        pl_df, pl_load_time = self._measure_time(
            lambda: pl.read_csv(self.data_path), "polars")
        
        self.console.log("Load csv: Done!")

        # Measure processing time for writing csv
        dir_path = os.path.dirname(self.data_path)
        pd_output_path = dir_path + "/pandas_output.csv"
        pl_output_path = dir_path + "/polars_output.csv"

        _, pd_write_time = self._measure_time(
            lambda: pd_df.to_csv(pd_output_path, index=False), "pandas")
        _, pl_write_time = self._measure_time(
            lambda: pl_df.write_csv(pl_output_path), "polars")
        
        self.console.log("Write csv: Done!")

        # Measure processing time for describing basic statistics
        _, pd_describe_time = self._measure_time(
            lambda: pd_df.describe(), "pandas")
        _, pl_describe_time = self._measure_time(
            lambda: pl_df.describe(), "polars")

        self.console.log("Describe basic statistics: Done!")
        
        # Measure processing time for filtering
        _, pd_filter_time = self._measure_time(
            lambda: pd_df[pd_df["numeric_val"] > 20.0], "pandas")
        _, pl_filter_time = self._measure_time(
            lambda: pl_df.filter(pl.col("numeric_val") > 20.0), "polars")
        
        self.console.log("Filter: Done!")

        # Measure processing time for removing missing values
        pd_df_removed, pd_remove_time = self._measure_time(
            lambda: pd_df.dropna(), "pandas")
        pl_df_removed, pl_remove_time = self._measure_time(
            lambda: pl_df.drop_nulls(), "polars")

        self.console.log("Remove null Done!")

        # Measure processing time for conversion
        _, pd_conversion_time = self._measure_time(
            lambda: pd_df_removed["numeric_val"].astype("int64"), "pandas")
        _, pl_conversion_time = self._measure_time(
            lambda: pl_df_removed.select(pl.col("numeric_val").cast(pl.Int64)), "polars")

        self.console.log("Conversion: Done!")

        # Measure processing time for One-Hot Encoding
        _, pd_encoding_time = self._measure_time(
            lambda: pd.get_dummies(pd_df["category_val"]), "pandas")
        _, pl_encoding_time = self._measure_time(
            lambda: pl_df.select(pl.col("category_val")).to_dummies(), "polars")

        self.console.log("One-Hot Encoding: Done!")

        # Measure processing time for sort
        _, pd_sort_time = self._measure_time(
            lambda: pd_df.sort_values(by="numeric_val", ascending=False), "pandas")
        _, pl_sort_time = self._measure_time(
            lambda: pl_df.sort("numeric_val", descending=True), "polars")

        self.console.log("Sort: Done...")
        

        # Add times into results dictionary
        results.update({
            "load csv": pd_load_time | pl_load_time,
            "write csv": pd_write_time | pl_write_time,
            "describe": pd_describe_time | pl_describe_time,
            "filter": pd_filter_time | pl_filter_time,
            "remove null": pd_remove_time | pl_remove_time,
            "conversion": pd_conversion_time | pl_conversion_time,
            "One-Hot Encoding": pd_encoding_time | pl_encoding_time,
            "Sort": pd_sort_time | pl_sort_time,
        })
        return results
