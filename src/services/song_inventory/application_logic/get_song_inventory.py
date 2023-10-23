from fastapi import HTTPException
from services.song_inventory.models.song_inventory import SongInventory
from database.db_config import db
from operator import attrgetter
from playhouse.shortcuts import model_to_dict
import datetime
from fastapi.encoders import jsonable_encoder

POSSIBLE_FILTER_PARAMS =  ['id','title','artist','duration']

def get_song_inventory(request):
    request = remove_unneccessary_params(request)

    search_params = get_search_params(request)
    
    if not search_params:
       raise HTTPException(status_code = 404, detail = 'search parameters are invalid') 
        
    song_inventory = get_song_inventory_data(request)
    
    return {
        'data' : song_inventory[0]
    }

def get_search_params(request):
    search_params = dict()
    if request.get('id') is not None:
        search_params['id'] = request.get('id')
        return search_params
    
    for search_key in ['title','artist','duration']:
        if request.get(search_key):
            search_params[search_key] = request.get(search_key)
    
    return search_params



def remove_unneccessary_params(request):
    filter_params = {}
    for param in POSSIBLE_FILTER_PARAMS:
        if request.get(param) is not None:
            filter_params[param] = request.get(param)
    return filter_params


def get_song_inventory_data(search_params):
    song_inventory = SongInventory.select()
    for key in search_params.keys():
        song_inventory = song_inventory.where(attrgetter(key)(SongInventory) == search_params[key])
                         
    song_inventory = jsonable_encoder(list(song_inventory.dicts()))
    
    if song_inventory is None:
        raise HTTPException(status_code = 404, detail = 'song inventory not found')
        
    return song_inventory
