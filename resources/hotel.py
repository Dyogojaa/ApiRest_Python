from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from flask import request
import sqlite3
import os

def normalize_path_params(**dados):
    cidade = dados.get('cidade', None)
    return {
        'estrelas_min': dados.get('estrelas_min', 0),
        'estrelas_max': dados.get('estrelas_max', 5),
        'diaria_min': dados.get('diaria_min', 0),
        'diaria_max': dados.get('diaria_max', 10000),
        'cidade': cidade.lower() if cidade else None,
        'limit': dados.get('limit', 50),
        'offset': dados.get('offset', 0)
    }

class Hoteis(Resource):
    def get(self):
        db_path = os.path.join('instance', 'banco.db')

        # Conectando-se ao banco de dados SQLite
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        dados = request.args
        parametros = normalize_path_params(**dados)

        print("Parametros antes da verificação de cidade:", parametros)

        consulta = "SELECT * FROM hoteis \
                    WHERE (estrelas BETWEEN ? AND ?) \
                    AND (diaria BETWEEN ? AND ?)"

        tupla = (
            parametros['estrelas_min'], parametros['estrelas_max'],
            parametros['diaria_min'], parametros['diaria_max']
        )

        if parametros['cidade']:
            print("Consulta com cidade")
            consulta += " AND LOWER(cidade) = ?"
            tupla += (parametros['cidade'],)

        consulta += " LIMIT ? OFFSET ?"
        tupla += (parametros['limit'] or 50, parametros['offset'] or 0)

        print("Tupla de parâmetros:", tupla)
        resultado = cursor.execute(consulta, tupla)

        hoteis = [
            {
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            }
            for linha in resultado
        ]

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
                
    

