from flask_restful import Resource, reqparse
from models.site import SiteModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from flask import request
import sqlite3
import os

class Sites(Resource):
   def get(self):
       return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        
        if site:
            return site.json()
        return {'mensagem': 'Site não encontrado'}, 404
    
    def post(self, url):
        if SiteModel.find_site(url):
           return {"mensagem": f"Site {url} já existe"}, 400

        site = SiteModel(url)        
        try:
            site.save()            
        except:
            return {"mensagem": f"Ocorreu um erro interno ao tentar criar um novo Site."}, 500        
        return site.json()
    
    def delete(self, url):
        site = SiteModel.find_site(url)
        
        if site:
            try:
                SiteModel.delete(site)
            except:
                return {"mensagem": f"Ocorreu um erro interno ao tentar excluir um novo Site."}, 500                                
            return {'mensagem': f'Site {url} Excluído com sucesso'}, 204
        
        return {'mensagem': 'Site não encontrado'}, 404
        
    