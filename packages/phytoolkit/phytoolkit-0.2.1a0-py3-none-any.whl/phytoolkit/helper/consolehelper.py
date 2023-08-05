"""Helper module for handling printing related functions."""
import click


class ConsoleHelper:
    """Different wrapper methods for printing output."""

    def __init__(self, log_file, verbose):
        self.log_file = log_file
        self.verbose = verbose

    def print(self, message, fg_color):
        """Prints the message in given colour."""
        click.secho(message, file=self.log_file, fg=fg_color)

    def verbose_print(self, message, fg_color):
        """Prints the message in given colour if verbose mode is enabled."""
        if self.verbose:
            self.print(message, fg_color)

    def info(self, message):
        """Prints the message in blue colour."""
        self.print(message, 'blue')

    def verbose_info(self, message):
        """Prints the message in blue colour if verbose mode is enabled."""
        self.verbose_print(message, 'blue')

    def success(self, message):
        """Prints the message in green colour."""
        self.print(message, 'green')

    def verbose_success(self, message):
        """Prints the message in green colour if verbose mode is enabled."""
        self.verbose_print(message, 'green')

    def error(self, message):
        """Prints the message in red colour to stderr/given file."""
        click.secho(message, file=self.log_file, fg='red', err=True)

    def verbose_error(self, message):
        """Prints the message in red colour to stderr/given file if verbose mode is enabled."""
        if self.verbose:
            click.secho(message, file=self.log_file, fg='red', err=True)
