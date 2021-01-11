from flask import Flask, render_template, request, redirect
import db
import math
from Websocket import SocketManager
import threading


app = Flask(__name__, static_url_path='/static')

def getHostname(request):
    from urllib.parse import urlparse
    o = urlparse(request.base_url)
    host = o.hostname
    return host

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/game', methods=['GET', 'POST'])
def game():
    
    if request.method == 'POST':
        playername = request.form['player_name']
        if not playername.isalnum():
            return render_template('index.html', playernameNotAllowed=True)
        
        return render_template('game_POST.html', hostname=getHostname(request), playername=playername)
    else:
        return render_template('game_GET.html', leaderboard=db.getLeaderboard())

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/monitoring')
def monitoring():
    playtime = math.ceil(db.getTotalPlaytime()/60)
    return render_template('monitoring.html', playtime=playtime, hostname=getHostname(request))

if __name__ == "__main__":
    webserver = threading.Thread(target=app.run, kwargs={'debug': True, 'host': "0.0.0.0", 'use_reloader': False})
    webserver.start()
    websocket = SocketManager()
    websocket.start()