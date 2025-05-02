from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, guardar_pedido, obtener_pedidos
from usuarios import crear_usuario, validar_usuario  # << agrega esto arriba
import os
import datetime

app = Flask(__name__)
app.secret_key = 'mango'  # Aquí sí va bien ✅

init_db()


@app.route('/')
def inicio():
    return redirect(url_for('menu'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order', methods=['POST'])
def order():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    producto = request.form.get('producto')

    if producto == "hamburguesa":
        ingredientes = request.form.getlist('ingredientes_hamburguesa')
    elif producto == "pizza":
        ingredientes = request.form.getlist('ingredientes_pizza')
    elif producto == "completo":
        ingredientes = request.form.getlist('ingredientes_completo')
    else:
        ingredientes = []

    ingredientes_str = ', '.join(ingredientes)

    guardar_pedido(nombre, telefono, producto, ingredientes_str)

    return render_template('thank_you.html', nombre=nombre, telefono=telefono)


@app.route('/thank-you')
def thank_you():
    nombre = request.args.get('nombre', 'Cliente')
    telefono = request.args.get('telefono', 'Sin número')
    return render_template('thank_you.html', nombre=nombre, telefono=telefono)

@app.route('/estado')
def estado():
    nombre = request.args.get('nombre', 'Cliente')
    telefono = request.args.get('telefono', 'Sin número')
    tiempo_recepcion = 1
    tiempo_preparacion = 8
    tiempo_retiro = 16

    return render_template('estado.html', nombre=nombre, telefono=telefono,
                           tiempo_recepcion=tiempo_recepcion,
                           tiempo_preparacion=tiempo_preparacion,
                           tiempo_retiro=tiempo_retiro)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validar_usuario(username, password):
            session['usuario'] = username
            return redirect(url_for('panel'))
        else:
            return "❌ Usuario o contraseña incorrecta."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/panel')
def panel():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    pedidos = obtener_pedidos()
    return render_template('panel.html', pedidos=pedidos)

@app.route('/crear-local', methods=['GET', 'POST'])
def crear_local():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        crear_usuario(usuario, contrasena)
        return "✅ Local creado exitosamente."
    return '''
        <form method="POST">
            Usuario: <input type="text" name="usuario" required><br>
            Contraseña: <input type="password" name="contrasena" required><br>
            <input type="submit" value="Crear Local">
        </form>
    '''

@app.route('/exportar')
def exportar():
    exportar_pedidos_a_txt()
    return "✅ Respaldo creado. Busca el archivo 'respaldo_pedidos.txt' en tu carpeta del proyecto."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


