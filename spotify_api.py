import pandas as pd
import requests
from tqdm.notebook import tqdm, trange
import math


def get_spotify(token, kind, elements=None, limit=50, offset=50, user=False):
    """
    token: Oath Token
    kind: Specify query kind albums, artists, tracks
    user: Specify whether the query involves a specific user
    elements (optional): Define spotify ids to query
    """
    limit = f'?limit={limit}'
    offset = f'&offset={offset}'
    query_kind = kind.lower()

    if user:
        endpoint_root = 'https://api.spotify.com/v1/me'
    else:
        endpoint_root = 'https://api.spotify.com/v1'

    if query_kind == 'albums':
        query = f'/artists?ids={elements}'

    elif query_kind == 'artists_albums':
        query = f'/artists/{elements}/albums'

    elif query_kind == "artists":
        query = f'/artists?ids={elements}'

    elif query_kind == 'user_tracks':
        query = f'/tracks'

    elif query_kind == 'album_tracks':
        query = f'/albums/{elements}/tracks'

    elif query_kind == 'audio-features':

        query = f'/audio-features?ids={elements}'

    elif query_kind == 'playlists':

        query = f'/playlists'

    elif query_kind == 'playlist_tracks':

        query = f'/playlists/{elements}/tracks'
    else:
        print("No Endpoint Located")

    if user:
        endpoint = endpoint_root + query + limit + offset

    else:
        endpoint = endpoint_root + query

    # https://api.spotify.com/v1/artists/{id}
    # https://api.spotify.com/v1/me/top/{type}
    # https://api.spotify.com/v1/audio-features
    # https://api.spotify.com/v1/tracks
    # https://api.spotify.com/v1/me/playlists
    # https://api.spotify.com/v1/playlists/{playlist_id}/tracks

    response = requests.get(url=endpoint, headers={'Authorization': 'Bearer ' + token}).json()

    if user:
        response_list = list()

        print(response.keys())

        print("Total Songs:", response['total'])
        print("Max Limit:", response['limit'])

        times = ((response['total'] - response['limit'])/response['limit'])

        print(times)

        response_list.append(response)

        for i in trange(math.floor(times)):

            response = requests.get(url=response['next'], headers={
                'Authorization': 'Bearer ' + token}).json()

            if response['next']:

                response_list.append(response)

            else:
                response_list.append(response)
                return response_list

    else:
        return response


def concat_df(response, albums=None):

    df = pd.DataFrame()

    for index, res in enumerate(tqdm(response)):

        df = pd.concat([df, pd.DataFrame(res)])

        if isinstance(albums, list):  # Album is a numpy array

            df['album_uri'] = albums[0][index]
            df['album_id'] = albums[1][index]

    return df


def date_parse_df(df, columns):

    for col in columns:

        df[f'{col}.year'] = pd.DatetimeIndex(df[col]).year
        df[f'{col}.month'] = pd.DatetimeIndex(df[col]).month
        df[f'{col}.day'] = pd.DatetimeIndex(df[col]).day

    return df
