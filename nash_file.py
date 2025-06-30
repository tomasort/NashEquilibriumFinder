#!/usr / bin/env python3
"""
Nash Equilibrium Finder - File-based CLI

A command line tool for analyzing 2 - player normal form games
defined in game definition files.
"""

import os
import sys
from pathlib import Path

import click

from normal_form.game_file_parser import GameFileParseError, GameFileParser
from normal_form.utils import (
    from_list_to_beliefs,
    get_coordinates_string,
    print_section_header,
    print_subsection_header,
)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Nash Equilibrium Finder - Analyze games from definition files."""
    pass


@cli.command()
@click.argument("game_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Choice(["normal", "minimal", "json"]),
    default="normal",
    help="Output format",
    show_default=True,
)
@click.option(
    "--analyze-mixed/--no-mixed", default=True, help="Whether to analyze mixed strategy equilibria for 2x2 games"
)
@click.option("--save-json", type=click.Path(), help="Save game data to JSON file")
def analyze(game_file, output, analyze_mixed, save_json):
    """
    Analyze a game defined in GAME_FILE.

    GAME_FILE should be a game definition file (see examples/ directory).
    """
    try:
        parser = GameFileParser()
        game_id, game = parser.parse_file(game_file)

        if output == "json":
            # JSON output
            game_data = parser.game_manager.export_game(game_id, format="json")
            click.echo(game_data)

            if save_json:
                with open(save_json, "w") as f:
                    f.write(game_data)
                click.echo(f"Game data saved to {save_json}", err=True)

            return

        # Analyze the game
        analysis = parser.game_manager.analyze_game(game_id, find_mixed=analyze_mixed)

        if output == "minimal":
            click.echo(f"Game from: {game_file}")
            click.echo(game.get_formatted_normal_form())
            nash_eq_coordinates = analysis.get("pure_nash", [])
            click.echo(f"\nPure Nash Equilibria: {get_coordinates_string(nash_eq_coordinates)}")

            if analyze_mixed and "mixed_nash" in analysis and game.rows == 2 and game.columns == 2:
                mixed_results = analysis["mixed_nash"]
                if isinstance(mixed_results, dict) and not mixed_results.get("error"):
                    p1_probs = mixed_results.get("p1_strategy")
                    p2_probs = mixed_results.get("p2_strategy")
                    if p1_probs and p2_probs:
                        click.echo(f"Mixed Nash: P1{p1_probs}, P2{p2_probs}")

            return

        # Normal detailed output
        print_section_header(f"Game Analysis: {os.path.basename(game_file)}")

        click.echo(f"File: {game_file}")
        click.echo(f"Game size: {game.rows}x{game.columns}")

        print_section_header("Normal Form")
        click.echo(game.get_formatted_normal_form())

        print_section_header("Pure Strategy Nash Equilibria")
        nash_eq_coordinates = analysis.get("pure_nash", [])
        click.echo(game.get_formatted_pure_nash())
        click.echo(f"\nPure Nash Equilibria: {get_coordinates_string(nash_eq_coordinates)}")

        # Mixed strategy analysis for 2x2 games
        if analyze_mixed and game.rows == 2 and game.columns == 2:
            print_section_header("Mixed Strategy Nash Equilibrium")

            if not nash_eq_coordinates:
                mixed_results = analysis.get("mixed_nash", {})

                if isinstance(mixed_results, dict):
                    p1_probs = mixed_results.get("p1_strategy")
                    p2_probs = mixed_results.get("p2_strategy")
                    error = mixed_results.get("error")

                    if error:
                        click.echo(f"Error: {error}")
                    else:
                        if p1_probs:
                            click.echo(f"Player 1 Mixed Strategy: {from_list_to_beliefs(p1_probs)}")
                            for i, prob in enumerate(p1_probs):
                                click.echo(f"  A{i + 1}: {prob:.3f}")

                        if p2_probs:
                            click.echo(f"\nPlayer 2 Mixed Strategy: {from_list_to_beliefs(p2_probs)}")
                            for i, prob in enumerate(p2_probs):
                                click.echo(f"  B{i + 1}: {prob:.3f}")
                else:
                    click.echo("Could not calculate mixed strategy Nash equilibrium.")
            else:
                click.echo("Pure strategy Nash equilibria exist.")

        if save_json:
            game_data = parser.game_manager.export_game(game_id, format="json")
            with open(save_json, "w") as f:
                f.write(game_data)
            click.echo(f"\nGame data saved to {save_json}")

    except GameFileParseError as e:
        click.echo(f"Error parsing game file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("game_file", type=click.Path(exists=True))
@click.option(
    "--p1-strategy",
    type=str,
    required=True,
    help="Player 1 mixed strategy as comma-separated probabilities (e.g., 0.3,0.7)",
)
@click.option(
    "--p2-strategy",
    type=str,
    required=True,
    help="Player 2 mixed strategy as comma-separated probabilities (e.g., 0.4,0.6)",
)
def payoffs(game_file, p1_strategy, p2_strategy):
    """
    Calculate expected payoffs for given mixed strategies.

    GAME_FILE should be a game definition file.
    """
    try:
        # Parse strategies
        p1_beliefs = [float(x.strip()) for x in p1_strategy.split(",")]
        p2_beliefs = [float(x.strip()) for x in p2_strategy.split(",")]

        # Validate probabilities
        if abs(sum(p1_beliefs) - 1.0) > 0.001 or any(x < 0 for x in p1_beliefs):
            click.echo("Error: Player 1 strategy must be valid probabilities summing to 1", err=True)
            sys.exit(1)

        if abs(sum(p2_beliefs) - 1.0) > 0.001 or any(x < 0 for x in p2_beliefs):
            click.echo("Error: Player 2 strategy must be valid probabilities summing to 1", err=True)
            sys.exit(1)

        # Parse game and calculate payoffs
        parser = GameFileParser()
        game_id, game = parser.parse_file(game_file)

        # Validate strategy dimensions
        if len(p1_beliefs) != game.rows:
            click.echo(f"Error: Player 1 strategy has {len(p1_beliefs)} values but game has {game.rows} rows", err=True)
            sys.exit(1)

        if len(p2_beliefs) != game.columns:
            click.echo(
                f"Error: Player 2 strategy has {len(p2_beliefs)} values but game has {game.columns} columns", err=True
            )
            sys.exit(1)

        # Calculate expected payoffs
        eps = parser.game_manager.calculate_expected_payoffs(game_id, p1_beliefs, p2_beliefs)

        print_section_header(f"Expected Payoffs: {os.path.basename(game_file)}")
        click.echo(f"Player 1 Strategy: {from_list_to_beliefs(p1_beliefs)}")
        click.echo(f"Player 2 Strategy: {from_list_to_beliefs(p2_beliefs)}")
        click.echo(f"\nExpected Payoff for Player 1: {eps[0]:.3f}")
        click.echo(f"Expected Payoff for Player 2: {eps[1]:.3f}")

    except ValueError as e:
        click.echo(f"Error parsing strategies: {e}", err=True)
        sys.exit(1)
    except GameFileParseError as e:
        click.echo(f"Error parsing game file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("game_file", type=click.Path(exists=True))
@click.option(
    "--player", type=click.Choice(["1", "2"]), required=True, help="Which player to analyze best responses for"
)
@click.option(
    "--opponent-strategy", type=str, required=True, help="Opponent mixed strategy as comma-separated probabilities"
)
def best_response(game_file, player, opponent_strategy):
    """
    Find best responses against an opponent's mixed strategy.

    GAME_FILE should be a game definition file.
    """
    try:
        # Parse opponent strategy
        beliefs = [float(x.strip()) for x in opponent_strategy.split(",")]

        # Validate probabilities
        if abs(sum(beliefs) - 1.0) > 0.001 or any(x < 0 for x in beliefs):
            click.echo("Error: Opponent strategy must be valid probabilities summing to 1", err=True)
            sys.exit(1)

        # Parse game
        parser = GameFileParser()
        game_id, game = parser.parse_file(game_file)

        player_num = int(player)

        # Validate strategy dimensions
        expected_dim = game.columns if player_num == 1 else game.rows
        if len(beliefs) != expected_dim:
            click.echo(f"Error: Opponent strategy has {len(beliefs)} values but expected {expected_dim}", err=True)
            sys.exit(1)

        # Calculate expected payoffs for each pure strategy
        expected_payoffs = game.find_br(player=player_num, mixing=True, beliefs=beliefs)

        print_section_header(f"Best Response Analysis: {os.path.basename(game_file)}")
        click.echo(f"Player {player} vs Opponent Strategy: {from_list_to_beliefs(beliefs)}")

        print_subsection_header(f"Player {player} Expected Payoffs")
        best_strategy = None
        best_payoff = None

        for strategy, payoff in expected_payoffs.items():
            click.echo(f"{strategy}: {payoff:.3f}")
            if best_payoff is None or payoff > best_payoff:
                best_payoff = payoff
                best_strategy = strategy

        click.echo(f"\nBest Response: {best_strategy} (Expected payoff: {best_payoff:.3f})")

    except ValueError as e:
        click.echo(f"Error parsing opponent strategy: {e}", err=True)
        sys.exit(1)
    except GameFileParseError as e:
        click.echo(f"Error parsing game file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("game_file", type=click.Path())
def validate(game_file):
    """
    Validate a game definition file.

    GAME_FILE should be a game definition file to validate.
    """
    if not os.path.exists(game_file):
        click.echo(f"Error: File '{game_file}' not found", err=True)
        sys.exit(1)

    parser = GameFileParser()
    warnings = parser.validate_file(game_file)

    if warnings:
        click.echo(f"Validation errors for {game_file}:", err=True)
        for warning in warnings:
            click.echo(f"  - {warning}", err=True)
        sys.exit(1)
    else:
        click.echo(f"✓ {game_file} is valid")


@cli.command()
def examples():
    """List available example game files."""
    examples_dir = Path(__file__).parent / "examples"

    if not examples_dir.exists():
        click.echo("No examples directory found")
        return

    game_files = list(examples_dir.glob("*.yml")) + list(examples_dir.glob("*.yaml"))

    if not game_files:
        click.echo("No example game files found")
        return

    click.echo("Available example game files:")
    click.echo("=" * 40)

    for game_file in sorted(game_files):
        click.echo(f"\n{game_file.name}")

        # Try to parse and show basic info
        try:
            parser = GameFileParser()
            game_id, game = parser.parse_file(str(game_file))
            click.echo(f"  Type: {game.mode if hasattr(game, 'mode') else 'Unknown'}")
            click.echo(f"  Size: {game.rows}x{game.columns}")

            # Show first few lines of the file
            with open(game_file) as f:
                lines = f.readlines()[:3]
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        click.echo(f"  {line}")
                        break
        except Exception:
            click.echo("  (Unable to parse)")

    click.echo("\nTo analyze an example:")
    click.echo("  nash - file analyze examples / prisoners_dilemma.yml")


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nProgram terminated by user.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\nUnexpected error: {e}", err=True)
        sys.exit(1)
