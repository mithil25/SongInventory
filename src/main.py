from typing import Union
from fastapi import FastAPI
from database.db_config import db
from database.insert_song_data import insert_song_inventory
from database.create_table import Table
from services.song_inventory.song_inventory_router import song_inventory_router
from services.song_inventory.models.song_inventory import SongInventory

app = FastAPI()

app.include_router(prefix = "/song_inventory" ,router = song_inventory_router)
@app.on_event("startup")
def start():
    if not db.connection():
         db.connect()
    if db.connection():
        Table.create_tables([SongInventory])
        print("The database connection is up...")
    
    

@app.on_event("shutdown")
def shutdown():
    print("The database connection is closed...")
    db.close()
    pass

@app.get("/")
def read_root():
    return "Welcome to Song Server!"

