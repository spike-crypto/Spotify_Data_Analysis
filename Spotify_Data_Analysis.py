import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector

print(mysql.connector.__version__)

# Setting up client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='b57fac04e5894fdc80aa7a2557e9cb5f',
    client_secret='fc2b1de953414776aa559deedffd5058'
))

# MySQL Database Connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'spotify_db'
}

# Connect to database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Reading the URL file path
file_path = "Track_url.txt"
with open(file_path, 'r') as file:
    Track_urls = file.readlines()  

# Processing each URL
for Track_url in Track_urls:
    Track_url = Track_url.strip()  
    
    try:
        track_id = re.search(r'track/([a-zA-Z0-9]+)', Track_url).group(1)
        track = sp.track(track_id)

        # Extract metadata
        track_data = {
            'Track_Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration_Minutes': track['duration_ms'] / 60000
        }

        # Insert data into MySQL
        insert_query = """
        INSERT INTO spotify_track (Track_Name, Artist, Album, Popularity, Duration_Minutes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            track_data['Track_Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration_Minutes']
        ))
        connection.commit()
        print(f"Inserted: {track_data['Track_Name']} by {track_data['Artist']}")

    except Exception as e:
        print(f"Error processing URL: {Track_url}, Error: {e}")  # Corrected print statement

# Close the connection
cursor.close()
connection.close()

print("All tracks are successfully inserted into the database.")
