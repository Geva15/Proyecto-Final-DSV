from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'uCEEoyKCKRnnUmAfifTHZJuXlMcKvODu'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 38549
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

@app.route('/lista_canciones')
def lista_canciones():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cancion, nombre_cancion, dificultad, notas FROM Canciones')
    canciones = cur.fetchall()
    cur.close()
    return render_template('lista_canciones.html', canciones=canciones)


@app.route('/cancion_facil/<int:cancion_id>')
def cancion_facil(cancion_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cancion, nombre_cancion, notas FROM Canciones WHERE id_cancion = %s', (cancion_id,))
    cancion = cur.fetchone()
    cur.close()
    return render_template('cancion_facil.html', cancion=cancion)

@app.route('/piano')
def pianoLibre():
    return render_template('piano_libre.html')

if __name__ == '__main__':
    app.run(port = 3000, debug=True)