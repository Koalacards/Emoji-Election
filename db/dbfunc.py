from typing import List, Optional

from db.dbmodel import ServerConfig


def set_election_channel_id(guild_id: int, election_channel_id: int):
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        ServerConfig.create(
            guild_id=guild_id,
            election_channel_id=election_channel_id,
            preview_channel_id=None,
            banned_list="[]",
        )
    else:
        update_query = ServerConfig.update(
            election_channel_id=election_channel_id
        ).where(ServerConfig.guild_id == guild_id)
        return update_query.execute()


def set_preview_channel_id(guild_id: int, preview_channel_id: int):
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        ServerConfig.create(
            guild_id=guild_id,
            election_channel_id=None,
            preview_channel_id=preview_channel_id,
            banned_list="[]",
        )
    else:
        update_query = ServerConfig.update(preview_channel_id=preview_channel_id).where(
            ServerConfig.guild_id == guild_id
        )
        return update_query.execute()


def get_election_channel_id(guild_id: int) -> Optional[int]:
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        return None
    else:
        for item in query:
            return item.election_channel_id


def get_preview_channel_id(guild_id: int) -> Optional[int]:
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        return None
    else:
        for item in query:
            return item.preview_channel_id


def get_banned_list_as_str(guild_id: int) -> str:
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        return "[]"
    else:
        for item in query:
            return item.banned_list


def set_banned_list_str(guild_id: int, banned_list_str: str):
    query = ServerConfig.select().where(ServerConfig.guild_id == guild_id)
    if len(query) == 0:
        ServerConfig.create(
            guild_id=guild_id,
            election_channel_id=None,
            preview_channel_id=None,
            banned_list=banned_list_str,
        )
    else:
        update_query = ServerConfig.update(banned_list=banned_list_str).where(
            ServerConfig.guild_id == guild_id
        )
        return update_query.execute()
