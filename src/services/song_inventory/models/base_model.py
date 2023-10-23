from peewee import *
from database.db_config import db
class BaseModel(Model):
    class Meta:
        database = db