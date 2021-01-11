import mysql.connector

database = mysql.connector.connect(
    host="oege.ie.hva.nl",
    user="biteld",
    password="ZcPnyn7ZhG$z0V",
    database="zbiteld",
)

def getLeaderboard():
    cursor = database.cursor()
    cursor.execute("SELECT `game_id`, `nickname`, `score`, `lives`, `date`, `time_played` FROM `Game` WHERE `score` > 0 ORDER BY `score` DESC LIMIT 10;")
    leaderboard = cursor.fetchall()
    database.commit()
    cursor.close()
    return leaderboard
    
def putGameRecord(info):
    cursor = database.cursor()
    sql = "INSERT INTO `Game` " \
          "(`nickname`, `score`, `lives`, `date`, `time_played`) " \
          "VALUES (%s, %s, %s, NOW(),%s);"
    timePlayed = "{:.2f}".format(info["timePlayed"])
    cursor.execute(sql, (info["playerName"], info["points"], info["lives"], timePlayed))
    database.commit()
    cursor.close()
    
def getTotalPlaytime():
    cursor = database.cursor()
    cursor.execute("SELECT SUM(`time_played`) FROM `Game`;")
    result = cursor.fetchone()
    database.commit()
    cursor.close()
    return result[0]