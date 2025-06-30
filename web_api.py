"""
Nash Equilibrium Finder - Web API

This is a simple Flask - based web API that demonstrates how
the refactored Nash Equilibrium Finder can be used in a web context.
"""

from flask import Flask, jsonify, request

from nash_equilibrium.game_manager import GameManager

app = Flask(__name__)
game_manager = GameManager()


@app.route("/api / games", methods=["POST"])
def create_game():
    """
    Create a new game.

    POST body parameters:
    - mode: 'r' (random) or 'd' (direct)
    - rows: Number of rows (if mode is 'r')
    - columns: Number of columns (if mode is 'r')
    - payoff_matrix: Payoff matrix (if mode is 'd')

    Returns:
    - game_id: ID of the created game - game: Game data in JSON format
    """
    data = request.json

    try:
        if data["mode"] == "d":
            # Direct payoff matrix mode
            game_id, game = game_manager.create_game(mode="d", payoff_matrix=data["payoff_matrix"])
        elif data["mode"] == "r":
            # Random mode
            game_id, game = game_manager.create_game(mode="r", rows=int(data["rows"]), columns=int(data["columns"]))
        else:
            return jsonify({"error": "Invalid mode"}), 400

        # Return the game data
        return jsonify({"game_id": game_id, "game": game.to_dict()})

    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api / common - games", methods=["POST"])
def create_common_game():
    """
    Create a common game type.

    POST body parameters:
    - game_type: Type of game ('prisoners_dilemma', 'coordination', etc.)
    - Additional parameters specific to the game type

    Returns:
    - game_id: ID of the created game - game: Game data in JSON format
    """
    data = request.json

    try:
        game_id, game = game_manager.create_common_game(
            game_type=data["game_type"], **{k: v for k, v in data.items() if k != "game_type"}
        )

        # Return the game data
        return jsonify({"game_id": game_id, "game": game.to_dict()})

    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api / games/<game_id>", methods=["GET"])
def get_game(game_id):
    """
    Get a game by ID.

    URL parameters:
    - game_id: ID of the game

    Returns:
    - game: Game data in JSON format
    """
    try:
        game = game_manager.get_game(game_id)
        return jsonify(game.to_dict())

    except KeyError:
        return jsonify({"error": f"Game with ID {game_id} not found"}), 404


@app.route("/api / games/<game_id>/analyze", methods=["GET"])
def analyze_game(game_id):
    """
    Analyze a game for Nash equilibria.

    URL parameters:
    - game_id: ID of the game

    Query parameters:
    - find_nash: Whether to find pure Nash equilibria (default: true)
    - find_mixed: Whether to calculate mixed strategy Nash equilibrium (default: true)

    Returns:
    - analysis: Analysis results
    """
    try:
        find_nash = request.args.get("find_nash", "true").lower() == "true"
        find_mixed = request.args.get("find_mixed", "true").lower() == "true"

        analysis = game_manager.analyze_game(game_id, find_nash=find_nash, find_mixed=find_mixed)

        return jsonify(analysis)

    except KeyError:
        return jsonify({"error": f"Game with ID {game_id} not found"}), 404


@app.route("/api / games/<game_id>/expected - payoffs", methods=["POST"])
def calculate_expected_payoffs(game_id):
    """
    Calculate expected payoffs with mixed strategies.

    URL parameters:
    - game_id: ID of the game

    POST body parameters:
    - p1_strategy: Player 1's mixed strategy (list of probabilities)
    - p2_strategy: Player 2's mixed strategy (list of probabilities)

    Returns:
    - expected_payoffs: [p1_payoff, p2_payoff]
    """
    data = request.json

    try:
        eps = game_manager.calculate_expected_payoffs(
            game_id, p1_strategy=data["p1_strategy"], p2_strategy=data["p2_strategy"]
        )

        return jsonify({"expected_payoffs": [float(eps[0]), float(eps[1])]})

    except KeyError as e:
        if str(e) == f"'{game_id}'":
            return jsonify({"error": f"Game with ID {game_id} not found"}), 404
        return jsonify({"error": str(e)}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api / games/<game_id>/random - beliefs", methods=["GET"])
def generate_random_beliefs(game_id):
    """
    Generate random mixed strategies.

    URL parameters:
    - game_id: ID of the game

    Query parameters:
    - mode: Method for generating random probabilities ('dirichlet' or 'sum', default: 'dirichlet')

    Returns:
    - beliefs: [p1_beliefs, p2_beliefs]
    """
    try:
        mode = request.args.get("mode", "dirichlet")

        beliefs = game_manager.generate_random_beliefs(game_id, mode=mode)

        return jsonify({"beliefs": [beliefs[0], beliefs[1]]})

    except KeyError:
        return jsonify({"error": f"Game with ID {game_id} not found"}), 404

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
