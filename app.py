from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  # Necesario para usar session
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Guardamos los datos en la sesión
        session.permanent = True
        session['nombre'] = request.form.get('nombre')
        session['telefono'] = request.form.get('telefono')
        return redirect(url_for('thank_you'))
    return render_template('order.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/estado')
def estado():
    nombre = request.args.get('nombre', 'Cliente')
    telefono = request.args.get('telefono', 'Sin número')

    # Puedes ajustar estos tiempos fácilmente
    tiempo_recepcion = 1    # en segundos
    tiempo_preparacion = 8
    tiempo_retiro = 16

    return render_template('estado.html', nombre=nombre, telefono=telefono,
                           tiempo_recepcion=tiempo_recepcion,
                           tiempo_preparacion=tiempo_preparacion,
                           tiempo_retiro=tiempo_retiro)


if __name__ == '__main__':
    app.run(debug=True)

