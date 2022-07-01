from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import re

app = Flask(__name__)

app.secret_key = 'Teletubies123'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Teletubies123'
app.config['MYSQL_DATABASE_DB'] = 'devices'
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect()
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM devices.user WHERE username = %s AND password = %s', (username, password,))
        usuarios = cursor.fetchone()
        conn.commit()
        if usuarios:
            session['loggedin'] = True
            session['id'] = usuarios[0]
            session['username'] = usuarios[1]
            return redirect('/home')
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect('/')

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect('/')

@app.route("/user")
def user():
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM devices.user;")
    usuarios = cursor.fetchall()
    conn.commit() 
    return render_template ('user.html', usuarios=usuarios)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM devices.user WHERE id=%s",(id))
    conn.commit() 
    return redirect("/user")

@app.route('/run')
def run():
    return render_template('/run.html')

if __name__ == "__main__":
    app.run(debug=True)