from flask import Flask, request, render_template,jsonify
app = Flask(__name__)
def do_something(text1,text2,text3,text4,score1,score2):
   text1 = text1.upper()
   text2 = text2.upper()
   combine= {}
   combine["hi"] = text1
   return combine
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    player1 = request.form['player1']
    word = request.args.get('player1')
    player2 = request.form['player2']
    player3 = request.form['player3']
    text4 = request.form['player4']
    score1 = request.form['score1']
    score2 = request.form['score2']
    combine = do_something(player1,player2,player3,text4,score1,score2)
    result = {
        "output": combine
    }
    print(result)
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)
if __name__ == '__main__':
    app.run(debug=True)