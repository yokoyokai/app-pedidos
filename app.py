from flask import Flask, render_template, request, redirect, url_for
from database import init_db, guardar_pedido, obtener_pedidos
import os
import datetime

app = Flask(__name__)

init_db()  # Esto se asegura de que la tabla 'pedidos' esté creada

@app.route('/')
def inicio():
    return redirect(url_for('menu'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        productos = request.form.getlist('producto')
        ingredientes = request.form.getlist('ingredientes')

        productos_str = ', '.join(productos)
        ingredientes_str = ', '.join(ingredientes)

        # Guardar en base de datos
        guardar_pedido(nombre, telefono, productos_str, ingredientes_str)

        return render_template('thank_you.html', nombre=nombre, telefono=telefono)

    return redirect(url_for('menu'))

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

@app.route('/panel')
def panel():
    pedidos = obtener_pedidos()
    return render_template('panel.html', pedidos=pedidos)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


