from fastapi import HTTPException
from services.song_inventory.models.song_inventory import SongInventory
from operator import attrgetter
from playhouse.shortcuts import model_to_dict
from database.db_config import db

def update_song_inventory(request):
    
    with db.atomic() as transaction:
        try:
            response = execute_song_inventory_data_transaction(request)
            return response
        except HTTPException as error:
            transaction.rollback()
            raise HTTPException(status_code = 404, detail = error)
        


def execute_song_inventory_data_transaction(request):
    
    search_params = get_search_params(request)
    
    if not search_params:
       return HTTPException(status = 404, detail = 'search parameters are invalid') 
        
    song_inventory = update_song_inventory_data(search_params,request)
    
    return {
        'id' : song_inventory.get('id')
    }

def get_search_params(request):
    search_params = dict()
    
    if request.get('id'):
        search_params['id'] = request.get('id')
        return search_params
    
    for search_key in ['title','artist','duration']:
        if request.get(search_key):
            search_params[search_key] = request.get(search_key)
    
    return search_params


def get_update_params(request):
    update_params = dict()
    for param in request.keys():
        if param not in ['id','title','artist','duration'] and request.get(param) is not None:
            update_params[param] = request.get(param)
    
    return update_params

def update_song_inventory_data(search_params,request):
    
    song_inventory = SongInventory.select(SongInventory.id)
    
    for key in search_params.keys():
        song_inventory = song_inventory.where(attrgetter(key)(SongInventory) == search_params[key])
    
    song_inventory = model_to_dict(song_inventory.first())
    if not song_inventory:
        return HTTPException(status_code = 404, detail = 'song inventory not found')
    
    update_params = get_update_params(request)
    if not update_params:
        return HTTPException(status_code = 404, detail = 'invalid update params')
    
    query = SongInventory.update(**update_params).where(SongInventory.id == song_inventory.get('id'))  
    
    try:
       query.execute()
    except Exception as error:
        return HTTPException(status_code = 404, detail = error)
        
    return song_inventory

