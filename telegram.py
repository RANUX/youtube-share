import telebot
from secret import TOKEN
from config import YOUTUBE_POST_URL, \
                    CHANNEL_NAME

def connect():
    return telebot.TeleBot(TOKEN)


def postYoutubeVideo(tbot, vid):
    link = '{!s}{!s}'.format(YOUTUBE_POST_URL, vid)
    tbot.send_message(CHANNEL_NAME, link)                    # post to telegram
