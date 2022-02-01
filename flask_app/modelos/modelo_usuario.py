from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask import flash
import re
from datetime import datetime

class Usuario:
    def __init__(self,id,first_name,last_name,birthday,email,password,created_at,updated_at):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.birthday=birthday
        self.email = email
        self.password=password
        self.created_at=created_at
        self.updated_at=updated_at
    
    @classmethod
    def agregaUsuario(cls,nuevoUsuario):
        query= "INSERT INTO usuarios (first_name,last_name,birthday,email,password) VALUES(%(first_name)s,%(last_name)s,%(birthday)s,%(email)s,%(password)s);"
        resultado = connectToMySQL("registro_usuarios").query_db(query,nuevoUsuario)
        print(resultado)
        return resultado
    
    @classmethod
    def verificaUsuario(cls, usuario):
        query= "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL("registro_usuarios").query_db(query,usuario)
        print("resultado",resultado)
        if len(resultado) > 0:
            usuarioResultado = Usuario(resultado[0]['id'],resultado[0]['first_name'],resultado[0]['last_name'],resultado[0]['birthday'],resultado[0]['email'],resultado[0]['password'],resultado[0]['created_at'],resultado[0]['updated_at'])
            print("aquiiii",usuarioResultado.password)
            return usuarioResultado
        else:
            return None
    
    @classmethod
    def validarRegistro(cls,registro):

        es_valido = True

        #Validando de que el email no exista en la BD
        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        resultado = connectToMySQL("registro_usuarios").query_db(query,registro)
        if len(resultado)>1:
            flash("Usuario ya se encuentra registrado", "registro")
            es_valido = False

        #Validando que el email tenga el formato adecuado
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(registro['email']):
            flash("El email es inválido, escribir un email correcto","registro")
            es_valido = False
        
        #Validando que el first_name tenga más de 2 caracteres
        if len(registro['first_name'])<2:
            flash("Incluir más de dos caracteres en el nombre","registro")
            es_valido = False

        #Validando que el first_name solo tenga letras
        NAME_REGEX= re.compile(r'^[a-zA-Z]+')
        if not NAME_REGEX.match(registro['first_name']):
            flash("El nombre debe incluir solo letras","registro")
            es_valido = False
        
        #Validando que el last_name tenga más de 2 caracteres
        if len(registro['last_name'])<2:
            flash("Incluir más de dos caracteres en el apellido","registro")
            es_valido = False
        
        #Validando que el last_name solo tenga letras
        if not NAME_REGEX.match(registro['last_name']):
            flash("El apellido debe incluir solo letras","registro")
            es_valido = False
        
        #Validando que el usuario tenga mayor de 10 años
        
        fecha_nac=datetime.strptime(registro['birthday'], '%Y-%m-%d')
        fecha_actual= datetime.today()
        edad= fecha_actual.year-fecha_nac.year
        if (fecha_actual.month,fecha_actual.day) < (fecha_nac.month,fecha_nac.day):
            edad -= 1
        print("EDAD:",edad)

        if edad < 10:
            flash("Solo se permite usuarios mayores de 10 años de edad", "registro")
            es_valido = False

        #Validande que la contraseña tenga al menos 8 caracteres, 1 letra mayúscula y 1 número
        PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        if not PASSWORD_REGEX.match(registro['password']):
            flash("La contraseña debe tener al menos 8 caracteres en total, incluyendo al menos 1 letra mayúscula y 1 número","registro")
            es_valido = False
        
        #Validando que las contraseñas coincidan
        if registro['password'] != registro['confirmPassword']:
            flash("Las contraseñas no coinciden","registro")
            es_valido = False
        
        #Validando que el cuadro de checkbox esté marcado
        if len(registro.getlist('check'))<1:
            flash("Por favor aceptar los términos","aceptarTerminos")
            es_valido = False
        
        return es_valido
        

        


