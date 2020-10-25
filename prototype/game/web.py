from flask import Flask, render_template
from Game import Game
app = Flask(__name__)


@app.route('/')
def index():
    game = Game(True)
    return render_template('index.html', variabele=game.playerLives, levens=game.GUN_DISTANCE_SAMPLES)

@app.route('/test')
def test():
    print("test")
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
