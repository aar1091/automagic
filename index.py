
#https://codeshack.io/login-system-python-flask-mysql/
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
 
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Teletubies123'
app.config['MYSQL_DATABASE_DB'] = 'devices'
mysql.init_app(app)

@app.route('/')
def index():
     return render_template ('auth.html')

@app.route("/login", methods=['POST'])
def login ():
    return redirect ('/main')

#Crear usuario
@app.route('/create')
def usuario():
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM devices.user;")
    usuarios = cursor.fetchall()
    conn.commit() 
    return render_template ('create.html', usuarios=usuarios)
    
#guardar usuarios
@app.route('/create', methods=['POST'])
def storage():
    _email = request.form['txtemail']
    _usuario = request.form['txtusuario']
    _passwrd = request.form['txtpasswd']
    
    sql ="INSERT INTO `devices`.`user` (`email`, `username`, `password`) VALUES (%s,%s,%s);"
    datos =(_email,_usuario,_passwrd)
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit() 
    return redirect ('/create')

#eliminar usuarios
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM devices.user WHERE id=%s",(id))
    conn.commit() 
    return redirect("/create")

#editar usuarios
@app.route('/editar/<int:id>')
def editar(id):
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM devices.user WHERE id=%s",(id))
    edituser = cursor.fetchall()
    cursor.execute("SELECT * FROM devices.user;")
    usuarios = cursor.fetchall()
    
    conn.commit() 
    return render_template("/edit.html",edituser = edituser, usuarios = usuarios)

#guardar usuarios
@app.route('/modificar', methods=['POST'])
def modify():
    _email = request.form['txtemail']
    _usuario = request.form['txtusuario']
    _passwrd = request.form['txtpasswd']
    _id = request.form['txtid']
    sql ="UPDATE devices.user SET email=%s, username=%s, password=%s WHERE id=%s;"
    datos =(_email,_usuario,_passwrd, _id)
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit() 
    return redirect ('/create')

@app.route('/main')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
