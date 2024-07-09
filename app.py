from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'estrella17'
app.config['MYSQL_DB'] = 'reportes'

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    vUsuario = request.form['txtUsuario']
    contrasena = request.form['passw']
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (vUsuario,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        stored_password = user[2]
        try:
            if bcrypt.checkpw(contrasena.encode('utf-8'), stored_password.encode('utf-8')):
                return redirect(url_for('Mostrar_reporte'))
            else:
                flash('Contraseña incorrecta', 'danger')
        except ValueError as ve:
            flash('Error interno al verificar la contraseña', 'danger')
    else:
        flash('Nombre de usuario no encontrado', 'danger')
    
    return redirect(url_for('Index'))

@app.route('/guardarGen_reporte', methods=['POST'])
def guardarGen_reporte():
    if request.method == 'POST':
        try:
            vNombre = request.form['txtNombre']
            vMatricula = request.form['txtMatricula']
            vLaboratorio = int(request.form['idlaboratorio'])
            vMaquina = int(request.form['idmaquina'])
            vDescripcion = request.form['txtDescripcion']

            cursor = mysql.connection.cursor()
            query = "INSERT INTO reportes (nombre, matricula, idlaboratorio, idmaquina, descripcion) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (vNombre, vMatricula, vLaboratorio, vMaquina, vDescripcion))
            mysql.connection.commit()
            cursor.close()

            flash('Reporte enviado correctamente', 'success')
            return redirect(url_for('mostrar_formulario'))
        except MySQLdb.Error as err:
            error_msg = f"Error al enviar el reporte: {err.args[0]} ({err.args[1]})"
            flash(error_msg, 'danger')
            app.logger.error(error_msg)
            return redirect(url_for('mostrar_formulario'))

@app.route('/gen_reporte', methods=['GET'])
def mostrar_formulario():
    success = request.args.get('success')
    if success:
        flash('Reporte enviado correctamente', 'success')
    return render_template('gen_reporte.html')

@app.route('/mostrar_reporte')
def Mostrar_reporte():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT r.id, r.idlaboratorio, r.idmaquina, r.fecha_reporte, r.descripcion, r.prioridad FROM reportes r JOIN laboratorios l ON r.idlaboratorio = l.id JOIN maquinas m ON r.idmaquina = m.id;')
    consulta = cursor.fetchall()
    return render_template('Reportes.html', reportes=consulta)

@app.route('/asignar_prioridad', methods=['POST'])
def asignar_prioridad():
    try:
        data = request.get_json()
        report_id = data.get('report_id')
        priority = data.get('priority')

        cursor = mysql.connection.cursor()
        query = "UPDATE reportes SET prioridad = %s WHERE id = %s"
        cursor.execute(query, (priority, report_id))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Priority updated successfully"})
    except MySQLdb.Error as err:
        error_msg = f"Error al actualizar la prioridad: {err.args[0]} ({err.args[1]})"
        app.logger.error(error_msg)
        return jsonify({"message": error_msg}), 500

@app.route('/consultar_reporte', methods=['GET', 'POST'])
def Consultar_reporte():
    if request.method == 'POST':
        reporte_id = request.form['reporte_id']
        nombre = request.form['nombre']
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT 
                r.id AS id_reporte, 
                r.nombre AS nombre_reporte, 
                r.descripcion, 
                CONCAT(e.nombre, ' ', e.apellido1, ' ', e.apellido2) AS nombre_completo_empleado, 
                s.nombre AS estatus_orden 
            FROM 
                reportes r 
            JOIN 
                orden_trabajos ot ON r.id = ot.idreporte 
            JOIN 
                empleados e ON ot.idempleado = e.id 
            JOIN 
                estatus s ON ot.idestatus = s.id
            WHERE r.id = %s AND r.nombre = %s;
        ''', (reporte_id, nombre))

        consulta = cursor.fetchall()
        cursor.close()
        
        return render_template('Consultar_reportes.html', consultar_reporte=consulta)
    return render_template('Consultar_reportes.html', consultar_reporte=None)

@app.route('/MostrarConsultar_reporte')
def MostrarConsultar_reporte():
    return render_template('Consultar_reportes.html')

if __name__ == '__main__':
    app.run(debug=True)
