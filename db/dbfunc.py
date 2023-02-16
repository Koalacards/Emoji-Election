from db.dbmodel import ServerConfig
from typing import Optional

def set_election_channel_id(guild_id:int, election_channel_id:int):
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        ServerConfig.create(guild_id=guild_id, election_channel_id=election_channel_id, preview_channel_id=None)
    else:
        update_query = ServerConfig.update(election_channel_id=election_channel_id).where(ServerConfig.guild_id == guild_id)
        return update_query.execute()


def set_preview_channel_id(guild_id:int, preview_channel_id:int):
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        ServerConfig.create(guild_id=guild_id, election_channel_id=None, preview_channel_id=preview_channel_id)
    else:
        update_query = ServerConfig.update(preview_channel_id=preview_channel_id).where(ServerConfig.guild_id == guild_id)
        return update_query.execute()


def get_election_channel_id(guild_id:int) -> Optional[int]:
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        return None
    else:
        for item in query:
            return item.election_channel_id


def get_preview_channel_id(guild_id:int) -> Optional[int]:
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        return None
    else:
        for item in query:
            return item.preview_channel_id