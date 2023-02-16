from peewee import *

database = SqliteDatabase('db/data.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class ServerConfig(BaseModel):
    election_channel_id = IntegerField(null=True)
    guild_id = IntegerField(null=True)
    preview_channel_id = IntegerField(null=True)

    class Meta:
        table_name = 'ServerConfig'
        primary_key = False

