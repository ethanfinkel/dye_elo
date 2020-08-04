"""Coded by Ethan Finkel on 7/24/20
This app takes inputs of two teams and the winner of the match. It then displays the ELO for each player and the change
"""
#imports
import math 
import sqlite3
from sqlite3 import Error
from flask import Flask, request, render_template,jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    global data
    select_all_data(conn)
    team1_player1 = request.form['player1']
    word = request.args.get('player1')
    team1_player2 = request.form['player2']
    team2_player1 = request.form['player3']
    team2_player2 = request.form['player4']
    score1 = int(request.form['score1'])
    score2 = int(request.form['score2'])
    score = score1-score2
    if score > 0:
        winner = 1
    else:
        winner = 0
    players = [team1_player1,team1_player2,team2_player1,team2_player2]
    elo = get_elo(players)
    team1= elo[0]+elo[1]
    team2 = elo[2] + elo[3] 
    sql_id = get_last_row_history()
    if sql_id:
        sql_id +=1
    else:
        sql_id = 1
    history[sql_id] = [team1_player1,data[team1_player1], team1_player2,data[team1_player2],score1,team2_player1,data[team2_player1],team2_player2,data[team2_player2],score2]
    change_1, change2 = EloRating(team1,team2,500,winner,score)
    update_elo(change_1,change2,players)
    for i in data:
        create_data(conn,[i,data[i]])
    i = sql_id
    create_history(conn,[sql_id,history[i][0],history[i][1],history[i][2],history[i][3],history[i][4],history[i][5],history[i][6],history[i][7],history[i][8],history[i][9]])
    output = {}
    for i in players:
        output[i] = i + " | " + str(round(data[i],0))

    return jsonify(result=output)

@app.route("/history")
def show_history():
    select_all_history(conn)
    return render_template("list.html", history = history)

@app.route("/leaderboard")
def leaderboard():
    select_all_data(conn)
    player_data = get_player_data()
    return render_template("leaderboard.html", players = player_data)

@app.route("/<slug>")
def search(slug):
    a =slug
    select_all_history(conn)
    select_all_data(conn)
    display_data = {}
    x = 0
    for i in history.values():
        for k in i:
            if k ==slug:
                x+=1
                display_data[x] = i
    player_data=get_player_data()
    score = player_data[slug]
    return render_template("player.html", history =display_data,score =score,slug=slug)


def get_player_data():
    players = sorted(data.items(), key=lambda x: x[1], reverse=True)
    player_data = {}
    x =1
    for i in players:
        player_data[i[0]] = [round(i[1],0),x]
        x+=1
    return player_data


def select_all_history(conn):
    global history
    cur = conn.cursor()
    cur.execute("SELECT * FROM history")
    rows = cur.fetchall()
    for k in rows:
        k = list(k)
        history[k[0]] = k[1:]

def select_all_data(conn):
    global data
    cur = conn.cursor()
    cur.execute("SELECT * FROM data")
    rows = cur.fetchall()
    for k, v in rows:
        data.setdefault(str(k),float(v))

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_data(conn, data):
    sql = ''' INSERT OR REPLACE INTO data(name,elo)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

def create_history(conn, history):
    sql = ''' INSERT INTO history(id,player1,player1_elo,player2,player2_elo,team1_score,player3,player3_elo,player4,player4_elo,team2_score)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, history)
    conn.commit()
    return cur.lastrowid

# Function to calculate the Probability 
def Probability(rating1, rating2): 
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 

def EloRating(Ra, Rb, K, d, s):    

    Pb = Probability(Ra, Rb) 
    Pa = Probability(Rb, Ra) 
    if (d == 1) : 
        change_1 = K * (1 - Pa) *s/12
        change_2 = K * (0 - Pb) * s/12
      
    else : 
        change_1 = K * (0 - Pa) *-s/12
        change_2 = K * (1 - Pb) *-s/12
    return change_1,change_2

def submit():
    database = r"/home/ubuntu/dye_elo/pythonsqlite.db"
    conn = create_connection(database)
    select_all_data(conn)
    print("Team 1")
    team1_player1= str(input("Player 1"))
    team1_player2 =str(input("Player 2"))
    print("Team 2")
    team2_player1= str(input("Player 1"))
    team2_player2 =str(input("Player 2"))
    score1 =int(input("Team 1 Score?"))
    score2 = int(input("Team 2 Score?")) 
    score = score1-score2
    if score > 0:
        winner = 1
    else:
        winner = 0
    players = [team1_player1,team1_player2,team2_player1,team2_player2]
    elo = get_elo(players)
    team1= elo[0]+elo[1]
    team2 = elo[2] + elo[3] 
    sql_id = get_last_row_history()
    if sql_id:
        sql_id +=1
    else:
        sql_id = 1
    history[sql_id] = [team1_player1,data[team1_player1], team1_player2,data[team1_player2],score1,team2_player1,data[team2_player1],team2_player2,data[team2_player2],score2]
    change_1, change2 = EloRating(team1,team2,500,winner,score)
    update_elo(change_1,change2,players)
    for i in data:
        create_data(conn,[i,data[i]])
    i = sql_id
    create_history(conn,[sql_id,history[i][0],history[i][1],history[i][2],history[i][3],history[i][4],history[i][5],history[i][6],history[i][7],history[i][8],history[i][9]])

def get_last_row_history():
    sql = '''SELECT max(id) FROM history;'''
    cur = conn.cursor()
    cur.execute(sql, history)
    a = cur.fetchall()
    a = list(a[0])
    a = a[0]
    return a

def get_elo(players):
    global data
    elo =[]
    for i in players:
         try:
            if data[i]:
                elo.append(data[i])
         except:
            data[i] = default_rating
            elo.append(default_rating)
    return elo

def update_elo(change_1, change_2, players):
    global data
    x = 0
    for i in players:
        if x <2:
            data[i] += change_1/2
        else:
            data[i] += change_2/2
        x+=1
        data[i] = round(data[i],1)
    print(change_1,change_2)
    for i in players:
        print(i,data[i])

def update_database_data(conn, data):
    sql = ''' UPDATE data
              SET elo = ?
              WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def display():
    for name in data:
        print (f"{name}, {data[name]:.2f}")
    for k in history:
        print(k,history[k])

#data import

#globals
data = {}
default_rating = 1000
history = {}

database = r"/home/ubuntu/dye_elo/pythonsqlite.db"
conn = sqlite3.connect(database, check_same_thread=False)
#main
select_all_data(conn)
select_all_history(conn)
if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)

