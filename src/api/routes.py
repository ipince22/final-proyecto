"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app #importamos current_app
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_mail import Message #importamos Message() de flask_mail
import random #importamos ramdom y string para generar una clave aleatoria nueva
import string


api = Blueprint('api', __name__)

#RECUPERACION CONTRASEÑA OLVIDADA 
@api.route("/forgotpassword", methods=["POST"])
def forgotpassword():
    recover_email = request.json['email']
    recover_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8)) #clave aleatoria nueva
    if not recover_email:
        return jsonify({"msg": "Debe ingresar el correo"}), 401
    #busco si el correo existe en mi base de datos
    user = User.query.filter_by(email=recover_email).first()
    if recover_email != user.email:
        return jsonify({"msg": "El correo ingresado no existe en nuestros registros"}), 400
    #si existe guardo la nueva contraseña aleatoria
    user.password = recover_password
    db.session.commit()
    #luego se la envio al usuario por correo para que pueda ingresar
    msg = Message("Hi", recipients=[recover_email])
    msg.html = f"""<h1>Su nueva contraseña es: {recover_password}</h1>"""
    current_app.mail.send(msg)
    return jsonify({"msg": "Su nueva clave ha sido enviada al correo electrónico ingresado"}), 200    

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200