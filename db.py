from peewee import SqliteDatabase, Model, CharField, BooleanField
from config import DB_NAME
import os.path

db = SqliteDatabase(DB_NAME)
db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class PublishedVideos(BaseModel):
    vid = CharField(unique=True)

def init_db_tables():
    db.create_tables([PublishedVideos])

def save_published_video(vid):
    PublishedVideos.create(vid=vid).save()

def get_publihed_video(vid):
    pub_video = None
    try:
        pub_video = PublishedVideos.get(PublishedVideos.vid == vid)
    except Exception:
        return None
    return pub_video.vid

def get_published_videos(count=5):
    return PublishedVideos.select().limit(count)

def init_db():
    if os.path.exists(DB_NAME):
        if not db.get_tables():
            print("Start init tables")
            init_db_tables()
            print("Done")

if __name__ == "__main__":
    init_db()