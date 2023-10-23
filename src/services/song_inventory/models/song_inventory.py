from peewee import *
import datetime
import uuid
from database.db_config import db
from services.song_inventory.models.base_model import BaseModel

class SongInventory(BaseModel):
    id = BigIntegerField(constraints=[SQL('AUTOINCREMENT')], primary_key=True)
    title = TextField()
    dance_ability = DecimalField(max_digits=20, decimal_places=10)
    energy = DecimalField(max_digits=10, decimal_places=10)
    accoustiness = DecimalField(max_digits=10, decimal_places=10)
    tempo = DecimalField(max_digits=20, decimal_places=10)
    duration = IntegerField()
    category = TextField()
    artist = TextField()
    rating = IntegerField(default = 0)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
      self.updated_at = datetime.datetime.now()
      if self.rating < 0:
         raise ValueError("Rating can't be negative") 
      if self.rating > 10:
        raise ValueError("rating can't be greater than 10")
      
      return super(SongInventory, self).save(*args, **kwargs)
  
    
    class Meta:
        table_name = "song_inventories"

    