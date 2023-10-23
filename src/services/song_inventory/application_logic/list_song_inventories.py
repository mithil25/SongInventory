from fastapi import HTTPException
from services.song_inventory.models.song_inventory import SongInventory
from operator import attrgetter
from playhouse.shortcuts import model_to_dict
import json
from math import ceil
from fastapi.encoders import jsonable_encoder

POSSIBLE_DIRECT_FILTERS = ['id','title','artist','duration','rating','energy','category','created_at','updated_at']

def list_song_inventories(filters, page_limit, page, sort_by, sort_type, pagination_data_required):
    if filters:
        if type(filters) != dict:
            filters = json.loads(filters)
            
    filters  = get_applicable_filters(filters)
    query = get_query(sort_by, sort_type)
    query = apply_filter(query, filters)
    query, total_count = apply_pagination(query, page, page_limit)

    pagination_data = get_pagination_data(
        query, page, page_limit, pagination_data_required, total_count
    )
    
    data = get_data(query)

    return {"list": data} | (pagination_data)


def get_query(sort_by, sort_type):
    query = SongInventory.select().order_by(eval("SongInventory.{}.{}()".format(sort_by, sort_type)))
    return query


def apply_pagination(query, page, page_limit):
    offset = (page - 1) * page_limit
    total_count = query.count()
    query = query.offset(offset).limit(page_limit)
    return query, total_count

def get_data(query):
    data = jsonable_encoder(list(query.dicts()))
    return data


def get_pagination_data(query, page, page_limit, pagination_data_required, total_count):
    if not pagination_data_required:
        return {}

    params = {
        "page": page,
        "total": ceil(total_count / page_limit),
        "total_count": total_count,
        "page_limit": page_limit,
    }
    
    return params

def apply_filter(query,filters):
    if not filters:
        return query
    for filter_key , filter_value  in filters.items():
        
        if isinstance(filter_value, bool):
            if filter_value:
                query = query.where(attrgetter(filter_key)(SongInventory))
            else:
                query = query.where(~attrgetter(filter_key)(SongInventory))
        elif isinstance(filter_value, str) or isinstance(filter_value, int):
            if filter_value != "":
                query = query.where(attrgetter(filter_key)(SongInventory) == filter_value)
        elif isinstance(filter_value, list):
            if 'None' in filter_value:
                filter_value.remove('None')
            attribute = getattr(SongInventory, filter_key)
            if isinstance(attribute, ArrayField):
                query = query.where(attrgetter(filter_key)(SongInventory).contains(filter_value))
            else:
                query = query.where(attrgetter(filter_key)(SongInventory) << filter_value)
        elif isinstance(filter_value, (str, type(None))):
            query = query.where(attrgetter(filter_key)(SongInventory) == filter_value)
    
    return query


def get_applicable_filters(filters):
    if not filters:
        return
    possible_filters = {}
    for filter_param in POSSIBLE_DIRECT_FILTERS:
        if filters.get(filter_param) is not None:
            possible_filters[filter_param] = filters.get(filter_param)
    
    return possible_filters
    
    