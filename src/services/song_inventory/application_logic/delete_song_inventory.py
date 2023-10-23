from fastapi import HTTPException
from services.song_inventory.models.song_inventory import SongInventory
from database.db_config import db
from operator import attrgetter
from playhouse.shortcuts import model_to_dict
from fastapi.encoders import jsonable_encoder


def delete_song_inventory(request):
    with db.atomic() as transaction:
        try:
            response = execute_song_inventory_data_transaction(request)
            return response
        except:
            transaction.rollback()
            raise 
    
def execute_song_inventory_data_transaction(request):
    search_params = get_search_params(request)
    
    if song_inventory_data_not_exists(search_params):
        raise HTTPException(status_code = 404, detail = 'Song Inventory data not exist')

    delete_song_inventory_data(search_params)
    
    return {
        'success' : 'True'
    }

def get_search_params(request):
    search_params = dict()
    
    if request.get('id') is not None:
        search_params['id'] = request.get('id')
        return search_params
    
    for search_key in ['title','artist','duration']:
        search_params[search_key] = request.get(search_key)
    
    return search_params


def delete_song_inventory_data(search_params):
    query = SongInventory.delete()
    for key, value in search_params.items():
        query = query.where(attrgetter(key)(SongInventory) == value)

    deleted_count = query.execute()
    if deleted_count == 0:
        raise HTTPException(status_code = 404, detail = 'Song Inventory deletion failed')

def song_inventory_data_not_exists(search_params):
    song_inventory = SongInventory.select(SongInventory.id)
    
    for key in search_params.keys():
        song_inventory = song_inventory.where(attrgetter(key)(SongInventory) == search_params[key])
            
    song_inventory_list = [item for item in song_inventory.dicts()] 
    
    if not song_inventory_list:  
        return True
    
    return False
