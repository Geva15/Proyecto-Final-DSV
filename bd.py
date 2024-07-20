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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('inicio'))

@app.before_request
def add_user_to_template():
    if 'username' in session:
        g.nombre = session['username']
    else:
        g.nombre = None


@app.route('/user_home')
def user_home():
    user_logged_in = g.nombre is not None
    cur = mysql.connection.cursor()
    imagen_barra = obtener_imagen_barra_y_puntos(g.nombre, cur)
    cur.close()
    return render_template('/Jugador/inicio.html', imagen_barra=imagen_barra, user_logged_in=user_logged_in)


def obtener_imagen_barra_y_puntos(nombre_usuario, db_cursor):
    # Obtener puntos totales del usuario
    db_cursor.execute('SELECT id FROM Usuario WHERE nombre = %s', (nombre_usuario,))
    usuario = db_cursor.fetchone()
    usuario_id = usuario['id']

    # Obtener los puntajes del usuario para cada canción
    db_cursor.execute('SELECT C.nombre_cancion, UC.puntos_obtenidos, C.puntos_totales FROM Usuario_Canciones UC JOIN Canciones C ON UC.id_cancion = C.id_cancion WHERE UC.id = %s', (usuario_id,))
    
    puntajes = db_cursor.fetchall()

    # Calcular la sumatoria total de los puntajes
    sumatoria_total = sum([p['puntos_obtenidos'] for p in puntajes])
    print(f'Sumatoria total de puntos del usuario {nombre_usuario}: {sumatoria_total}')
    # Obtener el total de puntos posibles
    db_cursor.execute('SELECT SUM(puntos_totales) AS puntos_totales FROM Canciones')
    total_puntos_posibles = db_cursor.fetchone()['puntos_totales']

    # Calcular el porcentaje para la barra de progreso
    porcentaje_progreso = sumatoria_total if total_puntos_posibles > 0 else 0

    if porcentaje_progreso < 280:
        imagen_barra = "barrita vacia.png"
    elif 280 <= porcentaje_progreso <=500:
        imagen_barra = "barrita primera estrella.png"
    elif 500 < porcentaje_progreso < 900:
        imagen_barra = "barrita primera estrella media.png"
    elif 900 <= porcentaje_progreso <=1200:
        imagen_barra = "barrita segunda estrella.png"
    elif 1200 < porcentaje_progreso < 1620:
        imagen_barra = "barrita segunda estrella media.png"
    elif porcentaje_progreso >= 1620:
        imagen_barra = "barrita tercera estrella.png"
    else:
        imagen_barra = "barrita tercera estrella.png"
    db_cursor.close()

    print(f'Porcentaje de progreso: {porcentaje_progreso}')
    print(f'Imagen de la barra seleccionada: {imagen_barra}')
    
    return imagen_barra


@app.route('/home')
def inicio():
    return render_template('/inicio.html')

@app.route('/piano')
def piano_libre():
    user_logged_in = g.nombre is not None
    cur = mysql.connection.cursor()
    imagen_barra = obtener_imagen_barra_y_puntos(g.nombre, cur)
    cur.close()
    return render_template('/Jugador/piano_libre.html', imagen_barra=imagen_barra, user_logged_in=user_logged_in)

@app.route('/teoria')
def teoria_notas():
    user_logged_in = g.nombre is not None
    cur = mysql.connection.cursor()
    imagen_barra = obtener_imagen_barra_y_puntos(g.nombre, cur)
    cur.close()
    return render_template('/Jugador/teoria_notas.html', imagen_barra=imagen_barra, user_logged_in=user_logged_in)

@app.route('/soporte')
def soporte():
    user_logged_in = g.nombre is not None
    cur = mysql.connection.cursor()
    imagen_barra = obtener_imagen_barra_y_puntos(g.nombre, cur)
    cur.close()
    return render_template('/Jugador/soporte.html', imagen_barra=imagen_barra, user_logged_in=user_logged_in)

@app.route('/lista_canciones')
def lista_canciones():
    user_logged_in = g.nombre is not None
    cur = mysql.connection.cursor()
    query = 'SELECT c.id_cancion, c.nombre_cancion, c.dificultad, c.notas, c.foto, COALESCE(uc.puntos_obtenidos, 0) AS puntaje_maximo FROM Canciones c LEFT JOIN Usuario_Canciones uc ON c.id_cancion = uc.id_cancion AND uc.id = (SELECT id FROM Usuario WHERE nombre = %s)'
    
    
    cur.execute(query, (g.nombre,))
    canciones = cur.fetchall()

    query_puntajes = '''
        SELECT c.id_cancion, COALESCE(uc.puntos_obtenidos, 0) AS puntaje_maximo
        FROM Canciones c
        LEFT JOIN Usuario_Canciones uc
        ON c.id_cancion = uc.id_cancion
        AND uc.id = (SELECT id FROM Usuario WHERE nombre = %s)
        ORDER BY c.id_cancion
    '''
    cur.execute(query_puntajes, (g.nombre,))
    puntajes = cur.fetchall()

    puntos_necesarios = [280, 620] 
    for i, cancion in enumerate(canciones):
        if i == 0:
            cancion['desbloqueada'] = True
        else:
            cancion['desbloqueada'] = puntajes[i-1]['puntaje_maximo'] >= puntos_necesarios[i-1]

    imagen_barra = obtener_imagen_barra_y_puntos(g.nombre, cur)

    cur.close()
    return render_template('/Jugador/lista_canciones.html', canciones=canciones, imagen_barra=imagen_barra, user_logged_in=user_logged_in)

@app.route('/cancion_facil/<int:cancion_id>')
def cancion_facil(cancion_id):
    user_logged_in = g.nombre is not None
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cancion, nombre_cancion, notas, puntos_totales FROM Canciones WHERE id_cancion = %s', (cancion_id,))
    cancion = cur.fetchone()
    
    imagen_barra = obtener_imagen_barra_y_puntos(g.nombre, cur)
    cur.close()
    return render_template('/Jugador/cancion_facil.html', cancion=cancion, imagen_barra=imagen_barra, user_logged_in=user_logged_in)

@app.route('/guardar_puntaje', methods=['POST'])
def guardar_puntaje():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        cancion_id = request.form['cancion_id']
        puntos_obtenidos = int(request.form['puntos_obtenidos'])
        
        
        print(f'Nombre de usuario: {nombre_usuario}, ID de canción: {cancion_id}, Puntaje: {puntos_obtenidos}')
        
        if not nombre_usuario or not cancion_id or not puntos_obtenidos:
            flash('Faltan datos necesarios.', 'error')
            return render_template('Jugador/inicio.html')
        
        cur = mysql.connection.cursor()
        
        try:
            # Obtener el id del usuario basado en su nombre
            cur.execute('SELECT id FROM Usuario WHERE nombre = %s', (nombre_usuario,))
            
            usuario = cur.fetchone()
            print(f'id usuario: {usuario}')
            
            
            if usuario:
                usuario_id = usuario['id']

                cur.execute('SELECT C.puntos_obtenidos FROM Usuario_Canciones C JOIN Usuario U ON C.id = U.id WHERE U.nombre = %s AND C.id_cancion = %s', (nombre_usuario, cancion_id))
                cancion = cur.fetchone()

                puntos_totales_actuales = int(cancion['puntos_obtenidos'])

                if puntos_obtenidos > puntos_totales_actuales:
                    # Actualizar puntaje en la base de datos
                    cur.execute('UPDATE Usuario_Canciones SET puntos_obtenidos = %s WHERE id_cancion = %s AND id = %s', (puntos_obtenidos, cancion_id, usuario_id))
                    mysql.connection.commit()
                    print(f'Filas afectadas: {cur.rowcount}')
                    flash('Puntaje actualizado exitosamente.', 'success')
                else:
                    flash('El puntaje obtenido no supera el puntaje actual.', 'info')
            else:
                flash('Usuario no encontrado.', 'error')
        except Exception as e:
            mysql.connection.rollback()
            print(f'Error al actualizar el puntaje: {e}')
            flash(f'Error al actualizar el puntaje: {e}', 'error')
        finally:
            cur.close()
        
        return redirect(url_for('inicio'))
    
@app.route('/piano_')
def piano_():
    return render_template('piano_libre.html')

@app.route('/teoria_')
def teoria_():
    return render_template('teoria_notas.html')

@app.route('/escala_')
def escala_():
    return render_template('escala.html')

@app.route('/soporte_')
def soporte_():
    return render_template('soporte.html')

@app.route('/lista_')
def lista_():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cancion, nombre_cancion, dificultad, foto, notas FROM Canciones')
    canciones = cur.fetchall()
    cur.close()
    user_logged_in = 'logged_in' in session
    return render_template('lista_canciones.html',canciones=canciones, user_logged_in=user_logged_in)
    

if __name__ == '__main__':
    app.run(debug=True, port=3000)
