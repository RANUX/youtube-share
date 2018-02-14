# -*- coding=utf-8 -*-

import httplib2
import os
import sys
import json
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from config import CLIENT_SECRETS_FILE, \
                    MISSING_CLIENT_SECRETS_MESSAGE, \
                    YOUTUBE_READONLY_SCOPE, \
                    YOUTUBE_API_SERVICE_NAME, \
                    YOUTUBE_API_VERSION, \
                    YOUTUBE_CHANNEL_ID

def remove_empty_kwargs(**kwargs):
    '''
    Remove keyword arguments that are not set
    '''
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs

def print_response(response):
    print(json.dumps(response, sort_keys=True, indent=2))

def get_youtube_client():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    message=MISSING_CLIENT_SECRETS_MESSAGE,
    scope=YOUTUBE_READONLY_SCOPE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

def activities_list(client, **kwargs):
    '''
    activities_list(youtube,
        part='snippet',
        channelId=YOUTUBE_CHANNEL_ID,
        maxResults=2)
    '''
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.activities().list(
    **kwargs
    ).execute()

    return print_response(response)

def videos_list_by_id(client, **kwargs):
    '''
    videos_list_by_id(client,
    part='snippet,contentDetails,statistics',
    id='Ks-_Mh1QhMc')
    videos_list_by_id(client, part='snippet',id=item['contentDetails']['upload']['videoId'])
    '''
    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.videos().list(
    **kwargs
    ).execute()

    return print_response(response)


def get_recent_video_ids(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.activities().list(**kwargs).execute()
    ids = []
    for item in response['items']:
        if item['kind'] == 'youtube#activity':
            if item['snippet']['type'] == 'upload':
                ids.append(item['contentDetails']['upload']['videoId'])
    
    return ids


def list_videos_in_all_playlists_by_channel_id(client, **kwargs):
    '''
    list_videos_in_all_playlists_by_channel_id(youtube,
        part='snippet',
        channelId=YOUTUBE_CHANNEL_ID,
        maxResults=25
    )
    '''
    response = client.playlists().list(
        **kwargs
    ).execute()
    
    for k in response['items']:
        print("Videos in list %s" % k['snippet']['localized']['title'])

        # Retrieve the list of videos uploaded to the authenticated user's channel.
        playlistitems_list_request = client.playlistItems().list(
            playlistId=k['id'],
            part="snippet",
            maxResults=10
        )

        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            # Print information about each video.
            for playlist_item in playlistitems_list_response["items"]:
                print(playlist_item)
                title = playlist_item["snippet"]["title"]
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                print("%s (%s)" % (title, video_id))

                playlistitems_list_request = client.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

def main():
    youtube_clinet = get_youtube_client()
    video_ids = get_recent_video_ids(
        youtube_clinet,
        part='snippet,contentDetails',
        channelId=YOUTUBE_CHANNEL_ID,
        maxResults=10
    )

    [print('https://youtube.com/watch?v={}'.format(id)) for id in video_ids]


if __name__ == '__main__':
    main()