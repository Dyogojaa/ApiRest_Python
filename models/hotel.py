class HotelModel:
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.cidade = cidade
        self.diaria = diaria
        
    def json(self):
        return {
             'hotel_id': self.hotel_id,
             'nome': self.nome,
             'estrelas': self.estrelas,
             'cidade': self.cidade,
             'diaria': self.diaria
         }
