from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json 

from services.song_inventory.song_params import *

from services.song_inventory.application_logic.get_song_inventory import get_song_inventory
from services.song_inventory.application_logic.create_song_inventory import create_song_inventory
from services.song_inventory.application_logic.delete_song_inventory import delete_song_inventory
from services.song_inventory.application_logic.update_song_inventory import update_song_inventory
from services.song_inventory.application_logic.list_song_inventories import list_song_inventories


song_inventory_router = APIRouter()

@song_inventory_router.get("/get_song_inventory")
def get_song_inventory_api(
    id: str = None,
    title: str = None,
    duration: int = None,
    artist: str = None,
    
):
    request = {
        'id' : id,
        'title': title,
        'duration': duration,
        'artist': artist,
    }
    data = get_song_inventory(request)
    return JSONResponse(status_code=200, content=data)

@song_inventory_router.post("/create_song_inventory")
def create_song_inventory_api(request: CreateSongInventory):
    try:
        data = create_song_inventory(request.dict())
        return JSONResponse(status_code=200, content =  data)
    except HTTPException as e:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )
        
@song_inventory_router.post("/delete_song_inventory")
def delete_song_inventory_api(request: DeleteSongInventory):
    try:
        data = delete_song_inventory(request.dict())
        return JSONResponse(status_code=200, content=json_encoder(data))
    except HTTPException as e:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )
        
# here filters is dictionary of song_inventory parameters in JSON STRING format
@song_inventory_router.get("/list_song_inventory")
def list_song_inventory_api(
    filters: str = '{"category":"relaxing","artist":"Coldplay"}',
    page_limit: int = 10,
    page: int = 1,
    sort_by: str = "created_at",
    sort_type: str = "asc",
    pagination_data_required: bool = True):
    try:
        data = list_song_inventories(
            filters, page_limit, page, sort_by, sort_type, pagination_data_required
            )
        return JSONResponse(status_code=200, content=data)
    except HTTPException as e:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )

@song_inventory_router.post("/update_song_inventory")
def update_song_inventory_api(request: UpdateSongInventory):
    try:
        data = update_song_inventory(request.dict())
        return JSONResponse(status_code=200, content= data)
    except HTTPException as e:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )
