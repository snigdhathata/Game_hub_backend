from flask import Flask, request, jsonify
from flask_cors import CORS

# ----------------------------
# IMPORT GAMES
# ----------------------------
from games import cartpoleFinal
from games import frozenlakeFinal
from games import gridworldFinal
from games import chessmulti
from games import fourinarowmulti
from games import numguessmulti

# ----------------------------
# APP SETUP
# ----------------------------
app = Flask(__name__)
CORS(app)

# ----------------------------
# GAME INSTANCES
# ----------------------------

# Number Guess Game
num_game = numguessmulti.BiDirectionalGuessingRL()

# Connect 4 Game
connect4 = fourinarowmulti.Connect4Game()
connect4_mode = "ai"   # or "pvp"

# ====================================================
# =============== AI GAME ROUTES (SPECIAL) ===========
# ====================================================

@app.route("/play/cartpole")
def play_cartpole():
    result = cartpoleFinal.run()
    return jsonify(result)

@app.route("/play/frozenlake")
def play_frozenlake():
    result = frozenlakeFinal.run()
    return jsonify(result)

@app.route("/play/gridworld")
def play_gridworld():
    result = gridworldFinal.run()
    return jsonify(result)

# ====================================================
# ===================== API ROUTES ===================
# ====================================================

# ----------------------------
# NUMBER GUESS GAME
# ----------------------------
@app.route("/api/numguess/ai", methods=["POST"])
def numguess_ai():
    data = request.json or {}
    result = num_game.ai_get_guess(
        low=data.get("low", 1),
        high=data.get("high", 100),
        level=data.get("level", "easy")
    )
    return jsonify(result)

@app.route("/api/numguess/user", methods=["POST"])
def numguess_user():
    data = request.json
    return jsonify(num_game.check_user_guess(data["guess"]))

@app.route("/api/numguess/reset", methods=["POST"])
def numguess_reset():
    num_game.reset()
    return jsonify({"status": "reset"})

# ----------------------------
# CONNECT 4 GAME
# ----------------------------
@app.route("/api/connect4/state")
def connect4_state():
    return jsonify({
        "board": connect4.board,
        "current_player": connect4.current_player,
        "game_over": connect4.game_over,
        "winner": connect4.winner,
        "mode": connect4_mode
    })

@app.route("/api/connect4/move", methods=["POST"])
def connect4_move():
    data = request.json
    col = data["column"]

    connect4.drop(col)

    if connect4_mode == "ai" and not connect4.game_over and connect4.current_player == 2:
        connect4.drop(connect4.ai_move())

    return jsonify({
        "board": connect4.board,
        "game_over": connect4.game_over,
        "winner": connect4.winner
    })

@app.route("/api/connect4/reset", methods=["POST"])
def connect4_reset():
    connect4.reset()
    return jsonify({"ok": True})

@app.route("/api/connect4/mode", methods=["POST"])
def connect4_mode_set():
    global connect4_mode
    connect4_mode = request.json.get("mode", "ai")
    connect4.reset()
    return jsonify({"mode": connect4_mode})

# ----------------------------
# CHESS GAME
# ----------------------------

@app.route("/api/chess/state", methods=["GET"])
def chess_state():
    return jsonify(chessmulti.get_state())

@app.route("/api/chess/start", methods=["POST"])
def chess_start():
    data = request.json or {}
    chessmulti.load_game(
        data.get("difficulty", "easy"),
        data.get("mode", "pvp")
    )
    return jsonify(chessmulti.get_state())

@app.route("/api/chess/player", methods=["POST"])
def chess_player():
    data = request.json
    result, status = chessmulti.player_move(data)
    return jsonify(result), status

@app.route("/api/chess/agent", methods=["POST"])
def chess_agent():
    return jsonify(chessmulti.agent_move())

# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
