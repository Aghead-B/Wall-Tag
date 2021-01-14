# dit is het bestand waar je begint.
from flask import Flask, render_template, request, redirect
import db
import math
from Websocket import SocketManager
import threading

#creert een instance van flask die de url naar de static folder afdwingt.
app = Flask(__name__, static_url_path='/static')

#gethostname parsed de host url en returned de hostname.
def getHostname(request):
    from urllib.parse import urlparse
    o = urlparse(request.base_url)
    host = o.hostname
    return host

#de index pagina
@app.route('/')
def index():
    return render_template('index.html')

# game checkt de methode indien dat 'post' wordt speler input gecontroleerd op alphanumerisch waarde.
@app.route('/game', methods=['GET', 'POST'])
def game():
    
    if request.method == 'POST':
        playername = request.form['player_name']
        if not playername.isalnum():
            return render_template('index.html', playernameNotAllowed=True)
        
        return render_template('game_POST.html', hostname=getHostname(request), playername=playername)
    else:
        return render_template('game_GET.html', leaderboard=db.getLeaderboard())

#about laad de over "..." pagina.
@app.route('/about')
def about():
    return render_template('about.html')

#monitoring haalt speeltijd op uit 'db' en rondt het af op de minuut.
@app.route('/monitoring')
def monitoring():
    playtime = math.ceil(db.getTotalPlaytime()/60)
    return render_template('monitoring.html', playtime=playtime, hostname=getHostname(request))

#als dit bestand uitgevoerd word dan run het deze code, komt het uit een import dan niet.
if __name__ == "__main__":
    webserver = threading.Thread(target=app.run, kwargs={'debug': True, 'host': "0.0.0.0", 'use_reloader': False})
    webserver.start()
    websocket = SocketManager()
    websocket.start()


