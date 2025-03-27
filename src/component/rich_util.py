from rich.console import Console
from rich.table import Table

class PrintResult:
    """
    Display a comparison table of processing times between pandas and polars
    using the Rich library.
    """

    def __init__(self) -> None:
        """
        Initializes the PrintResult instance with a Rich Console object.
        """
        self.console = Console()

    def display_comparison(self, results: dict[str, dict[str, float]]) -> None:
        """
        Displays a comparison table of processing times between pandas and polars.
        """
        if not results:
            self.console.print("[bold red]No results to display.[/bold red]")
            return

        # Create the table
        table = Table(
            title="Pandas vs Polars: Performance Comparison",
            caption="Ten measurements were taken and the averages were compared"
            )

        # Add columns
        table.add_column("Process", style="cyan", justify="left")
        table.add_column("pandas time (s)", style="cyan", justify="right")
        table.add_column("polars time (s)", style="cyan", justify="right")
        table.add_column("Faster Library", style="green", justify="right")

        # Add rows
        for process_type, result in results.items():
            pandas_time = result["pandas"]
            polars_time = result["polars"]
            faster_library = self.determine_faster_library(pandas_time, polars_time)
            table.add_row(
                process_type.capitalize(),
                f"{pandas_time:.6f}",
                f"{polars_time:.6f}",
                faster_library
            )

        # Display the table
        self.console.print(table)

    @staticmethod
    def determine_faster_library(pandas_time: float, polars_time: float) -> str:
        """
        Determines which library was faster for a given process.

        Args:
            pandas_time: Time taken by pandas.
            polars_time: Time taken by polars.

        Return:
            Name of the faster library or 'Tie' if both are equal.
        """
        if pandas_time < polars_time:
            return "pandas"
        elif polars_time < pandas_time:
            return "polars"
        else:
            return "Tie"
