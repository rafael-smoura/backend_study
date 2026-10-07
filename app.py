from flask import Flask, request, jsonify
from models.user import User
from dotenv import load_dotenv
from database import db
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from os import getenv

load_dotenv(".env")

DATABASE_URL = getenv("DATABASE_URL")
SECRET_KEY = getenv("SECRET_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Trata tentativas de acesso não autorizado em rotas protegidas
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"message": "Não autorizado. Faça login para acessar este recurso."}), 401

@app.route('/user/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if username and password:
        user = User.query.filter_by(username=username).first()
    
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "autenticação realizada com sucesso!"}), 200
    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"}), 200

@app.route('/user/create', methods=['POST'])
def create_user():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário Cadastrado com Sucesso!"}), 201

    return jsonify({"message": "Credenciais Inválidas"}), 400

@app.route('/user/read/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida"}), 403

    return jsonify({"username": user.username, "role": user.role}), 200

@app.route('/user/update/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json or {}
    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida"}), 403

    if data.get("password"):
        user.password = data.get('password')
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"}), 200

    return jsonify({"message": "Dados inválidos"}), 400

@app.route('/user/delete/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    if user:
        is_self_deletion = (current_user.id == user.id)

        if not is_self_deletion and current_user.role != "admin":
            return jsonify({"message": "Apenas administradores podem deletar outros usuários"}), 403
        
        db.session.delete(user)
        db.session.commit()

        if is_self_deletion:
            logout_user()

        return jsonify({"message": f"Usuário {id_user} removido com sucesso"}), 200
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/hello-world', methods=['GET'])
def principal():
    return "OLá mundo"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)