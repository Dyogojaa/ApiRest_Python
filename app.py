from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# Inicializa o banco de dados no contexto da aplicação Flask
with app.app_context():
    banco.init_app(app)
    banco.create_all()

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__':
    app.run(debug=True)
