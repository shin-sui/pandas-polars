import argparse
from pathlib import Path

import rootutils

from data.generate_data import generate_dataset
from component.compare import PandasPolarsComparator
from component.rich_util import PrintResult

def parse_args():
    """Parse command-line arguments to get the dataset filename.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing the dataset filename.
    """
    parser = argparse.ArgumentParser(description="Compare pandas and polars processing speeds.")
    parser.add_argument(
        "-d", "--dataset", type=str, default="sample_dataset.csv",
        help="Filename of the dataset to be used. Defaults to 'sample_dataset.csv'."
    )
    return parser.parse_args()

def main():
    """Entry point to orchestrate data retrieval, processing speed comparison, and result display.
    """
    args = parse_args()
    dataset_name = args.dataset

    # Find the root directory of the project
    root_path = rootutils.find_root(search_from=__file__, indicator=[".project-root"])
    data_path = Path(root_path) / "data" / dataset_name

    # Retrieve and save the dataset if it does not exist
    if not data_path.exists():
        generate_dataset(data_path)

    # Compare processing speeds between pandas and polars
    comparator = PandasPolarsComparator(data_path)
    results = comparator.compare()

    # Display the comparison results in a rich table format
    rich_output = PrintResult()
    rich_output.display_comparison(results)

if __name__ == "__main__":
    main()
