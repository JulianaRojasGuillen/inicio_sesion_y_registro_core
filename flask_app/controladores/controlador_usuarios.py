from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.modelos.modelo_usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app) #enviar el flask completo

@app.route ('/', methods=['GET'])
def inicio():
    return render_template("index.html")

@app.route('/registro', methods=['POST'])
def registro():

    if not Usuario.validarRegistro(request.form):
        return redirect('/')
    else:
        passwordEncriptado = bcrypt.generate_password_hash(request.form['password'])
        
        nuevoUsuario={
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "birthday":request.form['birthday'],
            "email": request.form['email'],
            "password": passwordEncriptado
        }

        #sesion
        session["first_name"] = request.form["first_name"]

        Usuario.agregaUsuario(nuevoUsuario)
        return redirect ('/dashboard')


@app.route('/login', methods=['POST'])
def login():

    loginPassword = request.form['loginPassword']

    usuario={
        "email": request.form['loginEmail'],
    }
    resultado = Usuario.verificaUsuario(usuario)
    if resultado == None:
        flash ("Email incorrecto", "login")
        return redirect ('/')
    else:
        if not bcrypt.check_password_hash(resultado.password, loginPassword):
            flash("El password es incorrecto", "login")
            return redirect('/')
        else:
            session['first_name'] = resultado.first_name
            return redirect ('/dashboard')

@app.route('/dashboard', methods=['GET'])
def despliegaDashboard():
    if 'first_name' in session:
        return render_template("dashboard.html",first_name=session['first_name'])
    else:
        return redirect ('/')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect ('/')