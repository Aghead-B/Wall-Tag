from flask import Flask, render_template, request, redirect, jsonify
from Game import Game
import mysql.connector

database = mysql.connector.connect(
    host="oege.ie.hva.nl",
    user="biteld",
    password="ZcPnyn7ZhG$z0V",
    database="zbiteld",
)


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

@app.route('/about')
def info():
    cursor = database.cursor()
    cursor.execute("SELECT `game_id`, `nickname`, `score`, `lives`, `date`, `time_played` FROM `Game` ORDER BY `score` DESC LIMIT 25;")
    results = cursor.fetchall()
    pagetitle = "Walltag"
    return render_template("about.html", mytitle=pagetitle, len = len(results), results = results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
