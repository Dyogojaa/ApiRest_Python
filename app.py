from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from sql_alchemy import banco
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


# Inicializa o banco de dados no contexto da aplicação Flask
with app.app_context():
    banco.init_app(app)
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_payload):
    print("Chegou na função verifica_blacklist.")
    jwt_id = jwt_payload['jti']
    print(f"Token ID em verifica_blacklist: {jwt_id}, BLACKLIST: {BLACKLIST}")
    return jwt_id in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return {'message': 'You have been logged out.'}, 401  # unauthorized


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    app.run(debug=True)
