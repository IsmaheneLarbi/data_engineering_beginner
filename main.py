import requests
import pandas as pd


from datetime import datetime, timedelta

# DATABASE_LOCATION = "sqlite://"
USER_ID = "Ismahene"
TOKEN = "BQDj-Wk7kSJGznOxzKS8m1mJ9TfIUBo6HIWjPtsJUl3ybPzjFXooGcl_q1hE_\
oUdIkbuEVMi9CW4xET0o1I4NRiRt_8tyYbVgErrRDnIwL1PcuJ0e3yGN7yXCU4iFzsQ7r7Z\
aeixHgFk0fTr0z2LKI9XHpvGkXz-C7Yd"

if __name__ == "__main__":
    headers = {
        "Accept" : "application/json",
        "Authorization" : f"Bearer {TOKEN}"
    }
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp() * 1000)
    response = requests.get(f"https://api.spotify.com/v1/\
me/player/recently-played?after={yesterday_unix_timestamp}", \
    headers=headers)
    data = response.json()
    songs = []
    albums = []
    artists = []
    played_at = []
    timestamps = []
    for item in data['items']:
        songs.append(item['track']['name'])
        albums.append(item['track']['album']['name'])
        artists.append(item['track']['artists'][0]['name'])
        played_at.append(item['played_at'])
        timestamps.append(item['played_at'][0:10])
    
    songs_dict = {
        'songs': songs,
        'albums': albums,
        'artists':artists,
        'played_at':played_at,
        'timestamps':timestamps
    }
    songs_df = pd.DataFrame(songs_dict)
    print(songs_df)
