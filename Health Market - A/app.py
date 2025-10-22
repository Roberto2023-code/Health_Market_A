from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, jsonify
from flask import send_from_directory
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from bson.json_util import dumps
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')  # Clave secreta más segura

# Configuración de la conexión a MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/market-health"
mongo = PyMongo(app)
db_consultas = mongo.db.Consultas



# Configuración para el manejo de archivos y extensiones permitidas
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}  # Permitimos más tipos de archivos

# Crear la carpeta 'uploads' si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# Función para verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Funciones de validación
def validar_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_password(password):
    """Valida fortaleza de contraseña"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una mayúscula"
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una minúscula"
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    return True, "Contraseña válida"

def validar_telefono(telefono):
    """Valida formato de teléfono"""
    pattern = r'^\+?1?-?\.?\s?\(?(\d{3})\)?[-\.\s]?(\d{3})[-\.\s]?(\d{4})$'
    return re.match(pattern, telefono) is not None



# CRUD Control de Cuentas (Admin, Cliente, User) CRUD
@app.route('/')
def index():
    admins = mongo.db.Clientes.find({"rol": "admin"})
    clientes = mongo.db.Clientes.find({"rol": "cliente"})
    users = mongo.db.Clientes.find({"rol": "user"})
    return render_template('pag-principal.html', admins=admins, clientes=clientes, users=users)

# Función auxiliar para verificar si el correo ya está registrado
def email_existe(email):
    return mongo.db.Clientes.find_one({"email": email}) is not None

@app.route('/insertAdmin', methods=['POST'])
def insert_admin():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    
    if email_existe(email):
        flash("El correo ya está registrado.", "error")
        return redirect(url_for('gestionar_cuentas'))
    
    # Hash de la contraseña
    password_hash = generate_password_hash(password)
    
    mongo.db.Clientes.insert_one({
        'nombre': nombre,
        'email': email,
        'password': password_hash,
        'rol': 'admin'
    })
    return redirect(url_for('gestionar_cuentas'))

@app.route('/insertCliente', methods=['POST'])
def insert_cliente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    password = request.form['password']
    telefono = request.form['telefono']
    fecha_nacimiento = request.form['fecha_nacimiento']
    genero = request.form['genero']
    
    if email_existe(email):
        flash("El correo ya está registrado.", "error")
        return redirect(url_for('gestionar_cuentas'))
    
    # Hash de la contraseña
    password_hash = generate_password_hash(password)
    
    mongo.db.Clientes.insert_one({
        'nombre': nombre,
        'apellido': apellido,
        'email': email,
        'password': password_hash,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'genero': genero,
        'rol': 'cliente'
    })
    return redirect(url_for('gestionar_cuentas'))

@app.route('/insertUser', methods=['POST'])
def insert_user():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    
    if email_existe(email):
        flash("El correo ya está registrado.", "error")
        return redirect(url_for('gestionar_cuentas'))
    
    # Hash de la contraseña
    password_hash = generate_password_hash(password)
    
    mongo.db.Clientes.insert_one({
        'nombre': nombre,
        'email': email,
        'password': password_hash,
        'rol': 'user'
    })
    return redirect(url_for('gestionar_cuentas'))

@app.route('/edit/<rol>/<user_id>', methods=['GET', 'POST'])
def edit_user(rol, user_id):
    user = mongo.db.Clientes.find_one({"_id": ObjectId(user_id)})
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        telefono = request.form.get('telefono')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        genero = request.form.get('genero')
        
        # Hash de la contraseña
        password_hash = generate_password_hash(password)
        
        update_data = {'nombre': nombre, 'email': email, 'password': password_hash, 'rol': rol}
        
        if rol == 'cliente':
            update_data.update({'telefono': telefono, 'fecha_nacimiento': fecha_nacimiento, 'genero': genero})
        
        mongo.db.Clientes.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        return redirect(url_for('gestionar_cuentas'))
    
    return render_template('edit-cliente.html', user=user, rol=rol)

@app.route('/delete/<user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    mongo.db.Clientes.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('gestionar_cuentas'))  # Cambié 'index' por 'gestionar_cuentas'





@app.route('/gestionar_cuentas')
def gestionar_cuentas():
    admins = list(mongo.db.Clientes.find({"rol": "admin"}))  # Convertir cursor a lista
    clientes = list(mongo.db.Clientes.find({"rol": "cliente"}))
    users = list(mongo.db.Clientes.find({"rol": "user"}))

    return render_template('CRUD_ctr-cuenta.html', admins=admins, clientes=clientes, users=users)




# Registro de usuario INCIO-PRINCIPAL
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        try:
            nombre = request.form.get("nombre", "").strip()
            apellido = request.form.get("apellido", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            telefono = request.form.get("telefono", "").strip()
            fecha_nacimiento = request.form.get("fecha_nacimiento", "")
            genero = request.form.get("genero", "")

            # Validaciones
            if not nombre or not apellido:
                flash("Nombre y apellido son obligatorios.", "error")
                return redirect(url_for("registro"))

            if not validar_email(email):
                flash("Formato de email inválido.", "error")
                return redirect(url_for("registro"))

            if email_existe(email):
                flash("El correo ya está registrado. Usa otro.", "error")
                return redirect(url_for("registro"))

            password_valida, mensaje_password = validar_password(password)
            if not password_valida:
                flash(mensaje_password, "error")
                return redirect(url_for("registro"))

            if telefono and not validar_telefono(telefono):
                flash("Formato de teléfono inválido.", "error")
                return redirect(url_for("registro"))

            # Hash de la contraseña
            password_hash = generate_password_hash(password)
            
            # Crea el usuario en la base de datos
            usuario = {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "password": password_hash,
                "telefono": telefono,
                "fecha_nacimiento": fecha_nacimiento,
                "genero": genero,
                "rol": "cliente",
                "fecha_registro": datetime.now()
            }
            mongo.db.Clientes.insert_one(usuario)

            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            flash("Error en el registro. Inténtalo de nuevo.", "error")
            return redirect(url_for("registro"))

    return render_template("registro.html")





# 🔹 RUTA PARA MANEJAR EL LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo_electronico = request.form.get("correo_electronico")
        contrasena = request.form.get("contrasena")

        # Buscar usuario en la base de datos
        usuario = mongo.db.Clientes.find_one({"email": correo_electronico})

        if usuario and check_password_hash(usuario["password"], contrasena):
            session["usuario"] = usuario["email"]  # Guardar usuario en sesión
            session["nombre_usuario"] = usuario["nombre"]  # Guardar nombre del usuario
            session["rol"] = usuario["rol"]  # Guardar el rol en sesión
            

            flash("Inicio de sesión exitoso.", "success")

            # Redirigir según el rol del usuario
            if usuario["rol"] == "admin":
                return redirect(url_for("gestionar_cuentas"))
            elif usuario["rol"] == "cliente":
                return redirect(url_for("pagina_principal"))
            elif usuario["rol"] == "user":
                return redirect(url_for("crudconsultass"))
            else:
                flash("Rol no reconocido.", "error")
                return redirect(url_for("login"))
        else:
            flash("Correo o contraseña incorrectos.", "error")
            return redirect(url_for("login"))

    return render_template("iniciosesion.html")


# 🔹 RUTA PARA ADMINISTRADORES (GESTIÓN DE CUENTAS)
@app.route("/gestionar-cuentas1")
def gestionar_cuentas1():
    if "usuario" not in session or session.get("rol") != "admin":
        flash("Acceso no autorizado. Inicia sesión como administrador.", "danger")
        return redirect(url_for("login"))

    return render_template("CRUD_ctr-cuenta.html")  # Ajusta el nombre de tu plantilla


# 🔹 RUTA PARA CLIENTES (PÁGINA PRINCIPAL)
@app.route("/pagina-principal")
def pagina_principal():
    if "usuario" not in session or session.get("rol") != "cliente":
        flash("Acceso no autorizado. Inicia sesión como cliente.", "danger")
        return redirect(url_for("login"))

    return render_template("pag-principal.html", nombre_usuario=session.get("nombre_usuario"))


# 🔹 RUTA PARA USUARIOS CON ROL "user" (GESTIÓN DE CONSULTAS MÉDICAS)
@app.route("/crudconsultass")
def crudconsultass():
    if "usuario" not in session or session.get("rol") != "user":
        flash("Acceso no autorizado. Inicia sesión como usuario.", "danger")
        return redirect(url_for("login"))

    return render_template("CRUD-consultas.html")



@app.route('/consultas')
def consultas():
    return render_template('consultas.html',nombre_usuario=session.get("nombre_usuario"))

#Boton de regreso a pag-principal de consultas.hmtl  (Lo mismo con el bt de regreso de productos.html a pag-principal)
@app.route('/principal')
def principal():
    return render_template('pag-principal.html',nombre_usuario=session.get("nombre_usuario"))

# Página principal Boton de inicio de sesion te redirije a iniciosesion.html
@app.route('/paguinaprincipal')
def insesion():
    return render_template('iniciosesion.html',nombre_usuario=session.get("nombre_usuario"))

# Página principal Boton de inicio de sesion te redirije a iniciosesion.html
@app.route('/crudcuen')
def sesion():
    return render_template('iniciosesion.html',nombre_usuario=session.get("nombre_usuario"))

#Paguina principal Boton de productos te redirije a productos.html
@app.route('/productos')
def productos():
    return render_template('productos.html',nombre_usuario=session.get("nombre_usuario"))

@app.route('/producto-detalle')
def producto_detalle():
    nombre = request.args.get('nombre')
    precio = request.args.get('precio')
    imagen = request.args.get('imagen')
    descripcion = request.args.get('descripcion')
    if not nombre:
        flash('Producto no especificado.', 'error')
        return redirect(url_for('productos'))
    return render_template('producto_detalle.html',
                           nombre=nombre,
                           precio=precio,
                           imagen=imagen,
                           descripcion=descripcion)

#Bt de regreso de CRUD-cuentas a iniciosesio.html
@app.route('/inise')
def inise():
    return render_template('iniciosesion.html',nombre_usuario=session.get("nombre_usuario"))

#Usuario cerrar sesión de pag-pricinpal, te redirige a iniciosesion.hmtl
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()  # Borra todos los datos de la sesión
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("login"))

#Ruta bt de perfil de pag-principal te redirige a perfil.html 
@app.route('/perfill')
def perfill():
        return render_template('perfil.html',nombre_usuario=session.get("nombre_usuario"))





# Ruta para agregar consulta consulta.html
@app.route('/agregar_consulta', methods=['GET', 'POST'])
def agregar_consulta():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        fecha_consulta = request.form['fecha_consulta']
        hora_consulta = request.form['hora_consulta']
        mensaje = request.form['mensaje']

        historial_medico_path = None  # Inicializar la variable del historial médico

        # Manejo del archivo de historial médico
        if 'historial_medico' in request.files:
            historial_medico = request.files['historial_medico']
            if historial_medico and historial_medico.filename:
                if allowed_file(historial_medico.filename):  # Verificar la extensión
                    filename = secure_filename(historial_medico.filename)
                    historial_medico_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    historial_medico.save(historial_medico_path)
                else:
                    flash('Formato de archivo no permitido. Solo se aceptan imágenes y documentos PDF/DOC.', 'danger')
                    return redirect(url_for('agregar_consulta'))

        # Insertar datos en MongoDB
        consulta = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "fecha_consulta": fecha_consulta,
            "hora_consulta": hora_consulta,
            "mensaje": mensaje,
            "historial_medico": historial_medico_path
        }

        mongo.db.Consultas.insert_one(consulta)

        # Mensaje de éxito
        flash('¡Consulta registrada con éxito! Nos pondremos en contacto contigo pronto.', 'success')

        return redirect(url_for('agregar_consulta'))

    return render_template('consultas.html')




# CRUD-consultas.html
# Ruta para mostrar y gestionar consultas
@app.route("/crud-consultas", methods=["GET", "POST"])
def crud_consulta():
    consultas = [{**consulta, "_id": str(consulta["_id"])} for consulta in mongo.db.Consultas.find()]  # Convertir cursor a lista
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        fecha_consulta = request.form["fecha"]
        hora_consulta = request.form["hora"]
        mensaje = request.form["mensaje"]

        # Manejo del archivo de historial médico
        historial_medico = None
        if 'historial_medico' in request.files:
            archivo = request.files['historial_medico']
            if archivo and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                historial_medico = f"uploads/{filename}"

        # Insertar la consulta en la base de datos
        mongo.db.Consultas.insert_one({
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "fecha_consulta": fecha_consulta,
            "hora_consulta": hora_consulta,
            "mensaje": mensaje,
            "historial_medico": historial_medico
        })
        
        return redirect(url_for("crud_consulta"))  # Redirigir a la misma página después de agregar

    # Pasar las consultas al template
    return render_template("CRUD-consultas.html", consultas=consultas)      # Siempre devuelve la lista

# Ruta para eliminar una consulta
@app.route("/delete-consulta/<consulta_id>", methods=["POST"])
def delete_consulta(consulta_id):
    mongo.db.Consultas.delete_one({"_id": ObjectId(consulta_id)})
    return redirect(url_for("crud_consulta"))

# Ruta para editar una consulta
@app.route("/edit-consulta/<consulta_id>", methods=["GET", "POST"])
def edit_consulta(consulta_id):
    consulta = mongo.db.Consultas.find_one({"_id": ObjectId(consulta_id)})
    
    if request.method == "POST":
        mongo.db.Consultas.update_one({"_id": ObjectId(consulta_id)}, {"$set": {
            "nombre": request.form["nombre"],
            "email": request.form["email"],
            "telefono": request.form["telefono"],
            "fecha_consulta": request.form["fecha"],
            "hora_consulta": request.form["hora"],
            "mensaje": request.form["mensaje"]
        }})
        return redirect(url_for("crud_consulta"))  # Redirigir después de la edición
    
    return render_template("edit-consulta.html", consulta=consulta)

# Para mostrar los archivos subidos, sirve el archivo si es solicitado
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/plan-alimentacion')
def plan_alimentacion():
    return render_template('plan_alimentacion.html')

@app.route('/contactos')
def contactos():
    return render_template('contacto.html')

@app.route('/pago')
def pago():
    return render_template('pago.html') 

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    return "Pago procesado con éxito. ¡Gracias por tu compra!"

@app.route("/perfil")
def perfil():
    # Simulación de datos; reemplázalos por los datos reales de tu sistema.
    datos_usuario = {
        "nombre_usuario": "Kevin",
        "correo_usuario": "kevin@example.com",
        "rol_usuario": "Cliente",
        "fecha_registro": "23 de marzo de 2025"
    }

    return render_template(
        "perfil.html",
        nombre_usuario=datos_usuario["nombre_usuario"],
        correo_usuario=datos_usuario["correo_usuario"],
        rol_usuario=datos_usuario["rol_usuario"],
        fecha_registro=datos_usuario["fecha_registro"]
    )

# Manejo de errores globales
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message="Página no encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Error interno del servidor"), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error_code=403, error_message="Acceso denegado"), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 