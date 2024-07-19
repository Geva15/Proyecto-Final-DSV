from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'uCEEoyKCKRnnUmAfifTHZJuXlMcKvODu'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 38549
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'llavecita'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('/Jugador/inicio.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        
        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'error')
            return render_template('register.html')
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT id FROM Usuario WHERE nombre = %s', (nombre,))
        usuario_existente = cur.fetchone()

        if usuario_existente:
            flash(f'EL usuario {nombre} ya esta registrado. Por favor, ingrese otro nombre.', 'error')
            cur.close()
            return render_template('register.html')
        
        cur.execute('INSERT INTO Usuario (nombre, contraseña) VALUES (%s, %s)', (nombre, password))
        mysql.connection.commit()
        cur.close()

        session['username'] = nombre

        return redirect(url_for('user_home', username=nombre))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Usuario WHERE nombre = %s AND contraseña = %s', (nombre, password))
        usuario = cur.fetchone()
        cur.close()

        if usuario:
            # Iniciar sesión correctamente
            session['username'] = nombre
            return redirect(url_for('user_home', username=nombre))
        else:
            # Mostrar un mensaje de error
            flash('Nombre de usuario o contraseña incorrectos', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.before_request
def add_user_to_template():
    if 'username' in session:
        g.nombre = session['username']
    else:
        g.nombre = None

@app.route('/user_home')
def user_home():

    return render_template('/Jugador/inicio.html')

@app.route('/piano')
def piano_libre():
    return render_template('/Jugador/piano_libre.html')

@app.route('/teoria')
def teoria_notas():
    return render_template('/Jugador/teoria_notas.html')

@app.route('/soporte')
def soporte():
    return render_template('/Jugador/soporte.html')

@app.route('/lista_canciones')
def lista_canciones():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cancion, nombre_cancion, dificultad, notas FROM Canciones')
    canciones = cur.fetchall()
    cur.close()
    return render_template('/Jugador/lista_canciones.html', canciones=canciones)

@app.route('/cancion_facil/<int:cancion_id>')
def cancion_facil(cancion_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cancion, nombre_cancion, notas, puntos_totales FROM Canciones WHERE id_cancion = %s', (cancion_id,))
    cancion = cur.fetchone()
    cur.close()
    return render_template('/Jugador/cancion_facil.html', cancion=cancion)

@app.route('/home')
def inicio():
    return render_template('/inicio.html')

@app.route('/piano_')
def piano_():
    return render_template('/piano_libre.html')

@app.route('/teoria_')
def teoria_():
    return render_template('/teoria_notas.html')

@app.route('/soporte_')
def soporte_():
    return render_template('/soporte.html')

@app.route('/lista_')
def lista_():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cancion, nombre_cancion, dificultad, notas FROM Canciones')
    canciones = cur.fetchall()
    cur.close()
    return render_template('/lista_canciones.html',canciones=canciones)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
