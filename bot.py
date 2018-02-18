# -*- coding=utf-8 -*-
import logging
from time import sleep
import time
from config import YOUTUBE_CHANNEL_ID, \
                    SLEEP_TIME
import sys
import db
import youtube as y2be
import vk
import telegram as tg

y2be_clinet = y2be.get_youtube_client()

# If True, use cron to run the script
# If False, the process starts and constantly running
SINGLE_RUN = False

# init bots
vkbot = vk.connect()
tbot = tg.connect()

def check_new_youtube_videos():
    video_ids = y2be.get_recent_video_ids(
        y2be_clinet,
        part='snippet,contentDetails',
        channelId=YOUTUBE_CHANNEL_ID,
        maxResults=10
    )

    for vid in video_ids:
        if db.get_publihed_video(vid):
            continue
        
        tg.postYoutubeVideo(tbot, vid)

        video_info = y2be.videos_list_by_id(y2be_clinet,
            part='snippet',
            id=vid
        )
        if video_info:
            playlist = y2be.get_playlist(y2be_clinet, 
                video_id=vid,
                part='snippet',
                channelId=YOUTUBE_CHANNEL_ID,
                maxResults=25
            )
            title = video_info['snippet']['localized']['title']
            desc  = video_info['snippet']['localized']['description'] + '\n' + \
                '#'+' #'.join(map(lambda x: ''.join(x.split()), video_info['snippet']['tags']))

            album = playlist['snippet']['title']
            vk.postYoutubeVideo(vkbot, vid, title, desc, album)

        db.save_published_video(vid)
        # We sleep a second to avoid all sorts of mistakes and limitations (just in case!)
        time.sleep(1)

if __name__ == '__main__':
    logging.info('[App] Run.\n')
    db.init_db()

    if not SINGLE_RUN:
        while True:
            check_new_youtube_videos()
            # Pause 4 minutes before re-checking
            logging.info('[App] Script went to sleep.')
            time.sleep(SLEEP_TIME)
    else:
        check_new_youtube_videos()
    
    logging.info('[App] Script exited.\n')