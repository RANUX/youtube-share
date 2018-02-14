# -*- coding=utf-8 -*-
import logging
from time import sleep
import time
from config import YOUTUBE_CHANNEL_ID, \
                    YOUTUBE_POST_URL, \
                    CHANNEL_NAME
from secret import TOKEN
import telebot
import sys
from youtube import get_youtube_client, get_recent_video_ids
import db

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
youtube_clinet = get_youtube_client()

# Если True, предполагается использование cron для запуска скрипта
# Если False, процесс запускается и постоянно висит запущенный
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
        # Спим секунду, чтобы избежать разного рода ошибок и ограничений (на всякий случай!)
        time.sleep(1)

if __name__ == '__main__':
    # Избавляемся от спама в логах от библиотеки
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    # Настраиваем наш логгер
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')

    logging.info('[App] Run.\n')
    db.init_db()

    if not SINGLE_RUN:
        while True:
            check_new_youtube_videos()
            # Пауза в 4 минуты перед повторной проверкой
            logging.info('[App] Script went to sleep.')
            time.sleep(60 * 4)
    else:
        check_new_youtube_videos()
    
    logging.info('[App] Script exited.\n')