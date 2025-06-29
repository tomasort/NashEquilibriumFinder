"""
Utility functions for Nash Equilibrium Finder

This module contains shared utility functions used across different
components of the Nash Equilibrium Finder project.
"""


def from_list_to_beliefs(lst):
    """Format a list of probabilities as a string representation of a belief vector."""
    belief = "("
    for i in range(len(lst)):
        belief += f"{lst[i]:.3f}"
        if i == len(lst) - 1:
            belief += ")"
        else:
            belief += ", "
    return belief


def get_coordinates_string(nash_eq_coordinates):
    """Format Nash equilibrium coordinates as a readable string."""
    if not nash_eq_coordinates:
        return "None"
    
    coordinates = ""
    for c in nash_eq_coordinates:
        # Display as 1-indexed for user-friendly output
        coordinates += f"(A{c[1] + 1}, B{c[0] + 1})   "
    return coordinates


def print_section_header(title):
    """Print a formatted section header."""
    try:
        import click
        click.echo(f"\n{'=' * 50}")
        click.echo(title)
        click.echo(f"{'=' * 50}")
    except ImportError:
        print(f"\n{'=' * 50}")
        print(title)
        print(f"{'=' * 50}")


def print_subsection_header(title):
    """Print a formatted subsection header."""
    try:
        import click
        click.echo(f"\n{'-' * 40}")
        click.echo(title)
        click.echo(f"{'-' * 40}")
    except ImportError:
        print(f"\n{'-' * 40}")
        print(title)
        print(f"{'-' * 40}")
