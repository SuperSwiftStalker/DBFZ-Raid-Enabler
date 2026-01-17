"""UI screen components and helpers.

This module contains reusable UI components for the TUI.
Currently minimal, but can be expanded for more complex screens.
"""

from rich.console import Console
from rich.panel import Panel
from rich import box


class ErrorScreen:
    """Display error messages."""

    @staticmethod
    def show_error(console: Console, title: str, message: str):
        """
        Display an error panel.

        Args:
            console: Rich console instance
            title: Error title
            message: Error message
        """
        panel = Panel(
            f"[red]{message}[/red]",
            title=f"[bold red]{title}[/bold red]",
            box=box.ROUNDED,
            border_style="red"
        )
        console.print(panel)


class InfoScreen:
    """Display informational messages."""

    @staticmethod
    def show_info(console: Console, title: str, message: str):
        """
        Display an info panel.

        Args:
            console: Rich console instance
            title: Info title
            message: Info message
        """
        panel = Panel(
            f"[cyan]{message}[/cyan]",
            title=f"[bold cyan]{title}[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan"
        )
        console.print(panel)


class WarningScreen:
    """Display warning messages."""

    @staticmethod
    def show_warning(console: Console, title: str, message: str):
        """
        Display a warning panel.

        Args:
            console: Rich console instance
            title: Warning title
            message: Warning message
        """
        panel = Panel(
            f"[yellow]{message}[/yellow]",
            title=f"[bold yellow]{title}[/bold yellow]",
            box=box.ROUNDED,
            border_style="yellow"
        )
        console.print(panel)
