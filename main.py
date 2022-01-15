import requests
import pandas as pd
import numpy as np


from datetime import datetime, timedelta

# DATABASE_LOCATION = "sqlite://"
TOKEN = "BQAzEL4kQ1OuIhOnBALwuTOhVPYpDriZPP7vMFW56JKTeW-Tcow4-3_nRWJlYQNesogUg8F0avl950APNFxXvq8dmJlMrxEOHjGGTvZBNfWo9LCUsT7Ujf2gd-dNxIBydDPUvdHpeqdp5kp4WY-4U6zME5nxLvFeoMB8"


def transform(df: pd.DataFrame) -> bool:
    """Returns True if data is valid, False if not."""
    if df.empty:
        print("No songs downloaded. Finishing execution.")
        return False
    if not pd.Series(df['played_at']).is_unique:
        raise Exception("Primary key check is violated.")
    if df.isnull().values.any():
        raise Exception("Null values found.")
    # yesterday = datetime.now() - timedelta(days=1)
    # yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    # timestamps = df['timestamps'].tolist()
    # for timestamp in timestamps:
    #     if datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
    #         raise Exception("At least one of the returned songs doesnt have a yesterday timestamp")
    return True


if __name__ == "__main__":
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
    songs_df = pd.DataFrame(songs_dict)
    print(songs_df)
    print(transform(songs_df))