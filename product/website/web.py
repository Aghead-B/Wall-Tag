from flask import Flask, render_template, request, redirect, jsonify
from Game import Game


app: Flask = Flask(__name__, static_url_path='/static')
game = Game(True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    game.playerName = request.form['player_name']
    if not game.playerName:
        return redirect('/')
    return redirect('/play')


@app.route('/get_data')
def get_data():
    return jsonify(playerName = game.playerName, playerLives=game.playerLives)


@app.route('/play')
def play():
    return render_template('update.html')


@app.route('/start')
def start():
    print("test start")
    game.start()
    return ''


@app.route('/quit')
def quit():
    print("test quit")
    game.quit()
    return ''


@app.route("/status")
def return_stat():
    print(game.targetStatus)
    return jsonify(targetStatus = game.targetStatus)


def return_lastline():
    lastline = game.lastline
    print(lastline)
    return jsonify(lastline)


@app.context_processor
def context_processor():
    return dict(lastline=return_lastline, return_stat=return_stat)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
