# SongInventory

SongInventory is a web application built using FastAPI and Peewee, utilizing an SQLite database to manage song inventory data. This project allows you to maintain a collection of songs, including their titles, artists, and other relevant information.

## Features

- Add new songs with details like title, artist,duration, category etc....
- Retrieve and display a list of all stored songs.
- Search for songs.
- Update and edit song details.
- Delete songs from the inventory.
- Update song rating 

## Technologies Used

- FastAPI: A modern, fast web framework for building APIs with Python.
- Peewee: A simple and expressive ORM for Python, used for managing the database.
- SQLite: A lightweight, serverless, and self-contained database engine.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Git (optional)

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/SongInventory.git
   cd SongInventory
2. Install dependencies
   pip3 install -r requirements.txt

3. Start Application:
   - cd src
   - python3 -m uvicorn main:app --reload
   - /docs in browser on the default host to for the swagger UI
   - /seed_song_data to seed 10 song_inventory
   - Explore the project 