from urllib.error import HTTPError
from click import echo
import requests
import pandas as pd
import sqlalchemy
import sqlite3


from datetime import datetime, timedelta
from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy_utils import database_exists


DATABASE_LOCATION = "sqlite:///my_spotify_data.sqlite"
TOKEN = ""


def is_data_valid(df: pd.DataFrame) -> bool:
    """Returns True if data is valid, False if not."""
    if df.empty:
        print("No songs downloaded. Finishing execution.")
        return False
    if not pd.Series(df['played_at']).is_unique:
        raise Exception("Primary key check is violated.")
    if df.isnull().values.any():
        raise Exception("Null values found.")
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamps = df['timestamps'].tolist()
    for timestamp in timestamps:
        if datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise Exception("At least one of the returned songs doesnt\
have a yesterday timestamp")
    return True


def load(df: pd.DataFrame):
    engine = sqlalchemy.create_engine(DATABASE_LOCATION, echo=True)
    con = engine.connect()
    metadata = MetaData()
    tracks = Table('my_played_tracks', metadata,
                   Column('song', String),
                   Column('artist', String),
                   Column('played_at', String, primary_key=True),
                   Column('timestamp', String))
    metadata.create_all(engine)
    print("Created database successfully.")
    df.to_sql('my_played_tracks', engine,
              index=False, if_exists='append')
    con.close()
    print("Closed database successfully.")


def extract():
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp() * 1000)
    response = requests.get(f"https://api.spotify.com/v1/\
me/player/recently-played?after={yesterday_unix_timestamp}",
                            headers=headers)
    # if response.status_code == 401:
    #     print("Your token has expired. Request a new one from spotify.")
    #     return None
    data = response.json()
    songs = []
    albums = []
    artists = []
    played_at = []
    timestamps = []
    print(data)
    for item in data['items']:
        songs.append(item['track']['name'])
        albums.append(item['track']['album']['name'])
        artists.append(item['track']['artists'][0]['name'])
        played_at.append(item['played_at'])
        timestamps.append(item['played_at'][0:10])

    songs_dict = {
        'songs': songs,
        'albums': albums,
        'artists': artists,
        'played_at': played_at,
        'timestamps': timestamps
    }
    return songs_dict


if __name__ == "__main__":
    songs_df = pd.DataFrame(extract())
    print(songs_df)
    if is_data_valid(songs_df):
        print("Data is valid, proceed to Load stage.")
        load(songs_df)
