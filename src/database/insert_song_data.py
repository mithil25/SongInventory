from config.song_seed_data import song_inventory
from services.song_inventory.application_logic.create_song_inventory import create_song_inventory
def insert_song_inventory():
    for song_inventory_data in song_inventory:
        try:
            create_song_inventory(song_inventory_data)
        except Exception as error:
            print(error)
            continue
    