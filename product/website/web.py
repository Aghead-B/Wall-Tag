from flask import Flask, render_template, request, redirect
from Game import Game
app = Flask(__name__, static_url_path='/static')
game = Game(True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods = ['POST'])
def signup():
    player_name = request.form['player_name']
    game.playerName = player_name
    game.start()
    return render_template('game.html')

@app.route('/update')
def update():
    return render_template('update.html', game=game)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
