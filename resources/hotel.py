from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
import sqlite3
import os


def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    def get(self):
        db_path = os.path.join('instance', 'banco.db')

        # Conectando-se ao banco de dados SQLite
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        print("Parametros antes da verificação de cidade:", parametros)

        if not parametros.get('cidade'):
            print("Consulta sem cidade")
            consulta = "SELECT * FROM hoteis \
                        WHERE (estrelas >= ? AND estrelas <= ?) \
                        AND (diaria >= ? AND diaria <= ?) \
                        LIMIT ? OFFSET ?"
            tupla = (parametros['estrelas_min'], parametros['estrelas_max'],
                     parametros['diaria_min'], parametros['diaria_max'],
                     parametros['limit'] or 50, parametros['offset'] or 0)
            print("Tupla de parâmetros:", tupla)
            resultado = cursor.execute(consulta, tupla)
        else:
            print("Consulta com cidade")
            consulta = "SELECT * FROM hoteis \
                        WHERE (estrelas >= ? AND estrelas <= ?) \
                        AND (diaria >= ? AND diaria <= ?) \
                        AND cidade = ? LIMIT ? OFFSET ?"
            tupla = (parametros['estrelas_min'], parametros['estrelas_max'],
                     parametros['diaria_min'], parametros['diaria_max'],
                     parametros['cidade'], parametros['limit'] or 50, parametros['offset'] or 0)
            print("Tupla de parâmetros:", tupla)
            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })

        print("Hoteis encontrados:", hoteis)

        return {'hoteis': hoteis}

                
class Hotel(Resource):    
    
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome',type=str, required=True, help='O campo nome não pode estar vazio')
    argumentos.add_argument('estrelas', type=float, required=True, help='O Campo Estrelas é obrigatório.')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    
    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:            
            return hotel.json()
        return {'message': 'Hotel não encontrado'}, 404
    @jwt_required()
    def post(self, hotel_id):
        
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel {hotel_id} já existe.'}, 400
        
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id=hotel_id, **dados)

        try:
            hotel.save()
            return hotel.json(), 201  # 201 Created
        
        except SQLAlchemyError as e:
            return {'message': f'Ocorreu um erro no banco de dados: {str(e)}'}, 500
        
    @jwt_required()
    def put(self, hotel_id):              
        dados = Hotel.argumentos.parse_args()         
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
                
        if hotel_encontrado:            
            hotel_encontrado.update(**dados)
            hotel_encontrado.save()
            return hotel_encontrado.json(), 200
        
        hotel = HotelModel(hotel_id, **dados) 
        try:
            hotel.save() 
            return hotel.json(), 201
        except SQLAlchemyError as e:
            return {'message': f'Ocorreu um erro no banco de dados: {str(e)}'}, 500            
        
    @jwt_required()
    def delete(self, hotel_id):
        
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:
            try:
                hotel.delete()            
                return {'message': 'Hotel apagado com sucesso'},204
            except SQLAlchemyError as e:
                return {'message': f'Ocorreu um erro no banco de dados: {str(e)}'}, 500            
        
        return {'message': 'Hotel não existe'},404
                
    

