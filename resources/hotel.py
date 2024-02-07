from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'cidade':'São Paulo',
        'estrelas': 4.3,
        'diaria':300
    },
    {
        'hotel_id': 'Beta',
        'nome': 'Beta Hotel',
        'cidade':'São Paulo',
        'estrelas': 4.0,
        'diaria':200
    },
    {
        'hotel_id': 'Giga',
        'nome': 'Giga Hotel',
        'cidade':'Rio de Janeiro',
        'estrelas': 5,
        'diaria':1300
    },
    {
        'hotel_id': 'Star',
        'nome': 'Star Hotel',
        'cidade':'Rio de Janeiro',
        'estrelas': 4.5,
        'diaria':350
    },
    {
        'hotel_id': 'Max',
        'nome': 'Max Hotel',
        'cidade':'Ribeirão Pires',
        'estrelas': 4.8,
        'diaria':560
    },
    {
        'hotel_id': 'Estancia',
        'nome': 'Estancia da Serra Hotel',
        'cidade':'Ribeirão Pires',
        'estrelas': 4.8,
        'diaria':560
    },
    
]

class Hoteis(Resource):
    def get(self):        
        return {'hoteis': hoteis}
                
class Hotel(Resource):
    
    
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('cidade')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        
        if hotel:            
            return hotel            
        return {'message': 'Hotel não encontrado'}, 404
                
    def post(self, hotel_id):
        
        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados) 
        novo_hotel = hotel_objeto.json()
        
        hoteis.append(novo_hotel)
        return novo_hotel, 200
    
        
    def put(self, hotel_id):      
        
        dados = Hotel.argumentos.parse_args()                
        hotel_objeto = HotelModel(hotel_id, **dados) 
        novo_hotel = hotel_objeto.json()
        
        hotel = Hotel.find_hotel(hotel_id)
                
        if hotel:            
            hotel.update(novo_hotel)
            return novo_hotel, 200
        
        hoteis.append(novo_hotel) 
        return novo_hotel, 201
    
    def delete(self, hotel_id):
        
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel apagado com sucesso'}
                
    
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel        
        return None

