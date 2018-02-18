# -*- coding: utf-8 -*-
import logging
import vk_api
import requests
from secret import VK_USER_LOGIN, VK_USER_PASSWORD
from config import VK_GROUP_ID, \
                    VK_GROUP_ID_NEG, \
                    YOUTUBE_POST_URL

def connect():
    vk_session = vk_api.VkApi(VK_USER_LOGIN, VK_USER_PASSWORD)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        logging.critical(error_msg)
        return

    return vk_session.get_api()

def addAlbum(vk, title):
    ''' Returns album id '''
    response = vk.video.addAlbum(group_id=VK_GROUP_ID, title=title, privacy='all')
    return response['album_id']

def getAlbum(vk, title, count='50'):
    ''' Returns
    {'id': 1, 'owner_id': -00000000, 'title': 'album title'}
    '''
    response = vk.video.getAlbums(owner_id=VK_GROUP_ID_NEG, count=count)
    if response['items']:
        for album in response['items']:
            if album['title'] == title:
                return album
    return None


def addVideoToGroupAlbum(vk, album_name, video_link, video_name='', video_description=''):
    '''Return video_id'''
    album = getAlbum(vk, album_name)
    if album:
        response = vk.video.save(name=video_name,
                                description=video_description,
                                link=video_link,
                                group_id=VK_GROUP_ID)
        if response['video_id']:
            r = requests.get(response['upload_url'])
            if r.status_code == 200:
                result = vk.video.addToAlbum(target_id=album['owner_id'],
                                    album_id=album['id'],
                                    owner_id=album['owner_id'],
                                    video_id=response['video_id'])
                if result == 1:
                    return response['video_id']
                else:
                    logging.error('Couldn\'t add video to %s' % album['owner_id'])
            else:
                logging.error('Couldn\'t call upload_url %s' % r)
        else:
            logging.error('Couldn\'t save video %s' % response)

    else:                                           # if album doesn't exists
        addAlbum(vk, album_name)
        return addVideoToGroupAlbum(vk, album_name, video_link, video_name, video_description)

def getVideoInfo(vk, title):
    response = vk.video.search(q=title)
    if response['items']:
        return response['items'][0]

    return None

def postVideoToGroupWall(vk, media_id, message):
    return vk.wall.post(owner_id=VK_GROUP_ID_NEG, message=message, attachments='video{}_{}'.format(VK_GROUP_ID_NEG, media_id))


def searchVideoOnWall(vk, title):
    return vk.wall.search(owner_id=VK_GROUP_ID_NEG, query='{}\n'.format(title))

def postYoutubeVideo(vk, vid, title, description, album_name):
    videoInfo = getVideoInfo(vk, title)

    if videoInfo:
        logging.info('Video already exists')
        response = searchVideoOnWall(vk, videoInfo['title'])
        if not response['items']:
            response = postVideoToGroupWall(vk, videoInfo['id'], '{}\n\n{}'.format(videoInfo['title'], videoInfo['description']))
            if response['post_id']:
                logging.info('Video successfuly posted to %s group wall' % VK_GROUP_ID)
            else:
                logging.error('Couldn\'t post video to %s group wall' % VK_GROUP_ID)
        else:
            logging.info('Video %s already posted' % videoInfo['title'])
    else:
        video_id = addVideoToGroupAlbum(vk,
                            album_name=album_name, 
                            video_link=YOUTUBE_POST_URL+vid,
                            video_name=title,
                            video_description=description
                            )

        if video_id:
            response = postVideoToGroupWall(vk, video_id, '{}\n\n{}'.format(title, description))
            if response['post_id']:
                logging.info('Video successfuly posted to %s group wall' % VK_GROUP_ID)
            else:
                logging.error('Couldn\'t post video to %s group wall' % VK_GROUP_ID)
        else:
            logging.warn('Couldn\'t post new video to wall')

def main():
    vk = connect()
    vid = 'BYSulHlHuxE'
    title = '5. Идентификаторы, строки, отступы и выражения. Основы Python'
    description = '''В уроке рассмотрены следующие темы:
                                        - что такое идентификатор'''
    album_name = 'Основы Python'
    postYoutubeVideo(vk, vid, title, description, album_name)


if __name__ == '__main__':
    main()