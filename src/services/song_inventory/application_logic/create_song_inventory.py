from fastapi import HTTPException
from services.song_inventory.models.song_inventory import SongInventory
from database.db_config import db
from operator import attrgetter
from playhouse.shortcuts import model_to_dict
import datetime

def create_song_inventory(request):
    with db.atomic() as transaction:
        try:
            response = execute_song_inventory_data_transaction(request)
            return response
        except:
            transaction.rollback()
            raise
    
def execute_song_inventory_data_transaction(request):
    search_params = get_search_params(request)
    
    if is_song_inventory_data_present(search_params):
        return HTTPException(status_code = 404, detail = 'Song Inventory data already exist')

    song_inventory_id = assign_attribute(request)
    
    return {
        'id' : song_inventory_id
    }

def get_search_params(request):
    search_params = dict()
    for search_key in ['title','artist','duration']:
        search_params[search_key] = request.get(search_key)
    return search_params


def assign_attribute(request):
    song_inventory_data = SongInventory.create(**request)
    song_inventory_data = model_to_dict(song_inventory_data)
    return song_inventory_data.get('id')

def is_song_inventory_data_present(search_params):
    song_inventory = SongInventory.select(SongInventory.id)
    for key in search_params.keys():
        song_inventory = song_inventory.where(attrgetter(key)(SongInventory) == search_params[key])
    
    if song_inventory.first():
        return True
    
    return False
