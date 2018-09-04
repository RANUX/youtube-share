
## About
Get latest published videos from YouTube channel and publish to:

* Telegram

## Install
Create `secret.py` and add TOKEN variable:
```
TOKEN = ''
```
Change `config.py` to your settings.
Run `make` in project folder, this will create virtualenv.

## Run
In project solder
```
source .venv/bin/activate
python bot.py
```

## Fixing errors
> ImportError: No module named 'oauth2client':
```
pip3 install --upgrade oauth2client
```

## YouTube
YouTube API quickstart:

https://developers.google.com/youtube/v3/quickstart/python

Useful links:

https://developers.google.com/youtube/v3/code_samples/python


## TODO:
Publish to:

* VK group