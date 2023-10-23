from fastapi import HTTPException
from services.song_inventory.models.song_inventory import SongInventory
from database.db_config import db
from operator import attrgetter


def delete_song_inventory(request):
    with db.atomic() as transaction:
        try:
            response = execute_song_inventory_data_transaction(request)
            return response
        except HTTPException as error:
            transaction.rollback()
            raise HTTPException(status_code = 404, detail = error)
    
def execute_song_inventory_data_transaction(request):
    search_params = get_search_params(request)
    
    if song_inventory_data_not_exists(search_params):
        return HTTPException(status_code = 404, detail = 'Song Inventory data not exist')

    delete_song_inventory_data(request)
    
    return {
        'success' : 'True'
    }

def get_search_params(request):
    search_params = dict()
    
    if request.get('id'):
        search_params['id'] = request.get('id')
        return search_params
    
    for search_key in ['title','artist','duration']:
        search_params[search_key] = request.get(search_key)
    
    return search_params


def delete_song_inventory_data(search_params):
    song_inventory_data = SongInventory.delete()
    for key in search_params.keys():
        song_inventory_data = song_inventory_data.where(attrgetter(key)(SongInventory) == search_params[key])
    
    pass

def song_inventory_data_not_exists(search_params):
    song_inventory = SongInventory.select(SongInventory.id)
    for key in search_params.keys():
        song_inventory = song_inventory.where(attrgetter(key)(SongInventory) == search_params[key])
    
    if song_inventory.first():
        return True
    
    return False
