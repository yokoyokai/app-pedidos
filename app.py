from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)

@app.route('/')
def inicio():
    return redirect(url_for('menu'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order', methods=['POST'])
def recibir_pedido():
    nombre = request.form.get('nombre', 'Cliente')
    telefono = request.form.get('telefono', 'Sin número')
    producto = request.form.get('producto', 'Sin producto')
    ingredientes = request.form.getlist('ingredientes')

    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pedido = f"""
==== NUEVO PEDIDO ====
Fecha y hora: {fecha_hora}
Nombre: {nombre}
Teléfono: {telefono}
Producto: {producto}
Ingredientes modificados: {', '.join(ingredientes)}
------------------------
"""

    with open("pedidos.txt", "a", encoding="utf-8") as archivo:
        archivo.write(pedido)

    return redirect(url_for('thank_you', nombre=nombre, telefono=telefono))

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


