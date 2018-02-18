# -*- coding=utf-8 -*-
import logging
from time import sleep
import time
from config import YOUTUBE_CHANNEL_ID, \
                    YOUTUBE_POST_URL, \
                    CHANNEL_NAME, \
                    SLEEP_TIME
from secret import TOKEN
import telebot
import sys
from youtube import get_youtube_client, get_recent_video_ids
import db

youtube_clinet = get_youtube_client()

# If True, use cron to run the script
# If False, the process starts and constantly running
SINGLE_RUN = False

bot = telebot.TeleBot(TOKEN)

def check_new_youtube_videos():
    video_ids = get_recent_video_ids(
        youtube_clinet,
        part='snippet,contentDetails',
        channelId=YOUTUBE_CHANNEL_ID,
        maxResults=10
    )

    for vid in video_ids:
        if db.get_publihed_video(vid):
            continue
        
        link = '{!s}{!s}'.format(YOUTUBE_POST_URL, vid)
        bot.send_message(CHANNEL_NAME, link)
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