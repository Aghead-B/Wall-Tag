from flask import Flask, render_template, request, redirect, jsonify
from Game import Game


app = Flask(__name__, static_url_path='/static')
game = Game(True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    game.playerName = request.form['player_name']
    if not game.playerName:
        return redirect('/')
    game.start()
    return render_template('update.html', game=game)


@app.route('/get_data', methods=['GET'])
def get_data():

    return jsonify(playerName=game.playerName,
                   playerPoints=game.playerPoints,
                   playerLives=game.playerLives,
                   lastLine=game.lastLine)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
