from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    def get(self):        
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
                
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
                
    

