from pydantic import BaseModel
from peewee import *
from typing import Optional,List
from datetime import datetime

class CreateSongInventory(BaseModel):
    title: str 
    dance_ability: str 
    energy: str 
    accoustiness: str 
    tempo: str 
    duration: str 
    category: str 
    artist: str 

class DeleteSongInventory(BaseModel):
    id: int =  None
    title: str =  None
    artist: str =  None
    duration: str =  None
    

class UpdateSongInventory(BaseModel):
    id: int =  None
    title: str =  None
    dance_ability: float = None 
    energy: float = None
    accoustiness: float = None
    tempo: float = None
    duration: int =  None
    category: str = None
    artist: str =  None
    rating: int = None