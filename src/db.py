from typing import List
from aiohttp import ClientSession
from pydantic import BaseModel
from orjson import loads


class GuildSettings(BaseModel):
    id: int
    log_channel: int
    summary_channel: int
    notify_users: List[int]


class GuildMetrics(BaseModel):
    guild_id: int
    members: int
    bans: int
    kicks: int
    total_events: int
    timeouts: int


class SupaClient:
    def __init__(self, supabase_url, supabase_key):
        self.http = ClientSession(
            base_url=supabase_url,
            headers={"apikey": supabase_key, "Authorization": f"Bearer {supabase_key}"},
        )

    async def __request(self, method, url, data=None, **kwargs):
        r = await self.http.request(method, f"/rest/v1{url}", data=data, **kwargs)
        r.raise_for_status()
        try:
            return loads(await r.text())
        except:
            return None

    async def get_settings(self, guild_id: int) -> GuildSettings:
        r = await self.__request("GET", f"/settings?id=eq.{guild_id}")
        return GuildSettings(**loads(await r.text()))  # type: ignore

    async def update_settings(self, guild_id: int, settings: GuildSettings):
        r = await self.__request(
            "POST",
            f"/settings?id=eq.{guild_id}",
            data=settings.dict(),
            headers={"Prefer": "resolution=merge-duplicates"},
        )
        print(r)

    async def send_metrics(self, guild_id: int, metrics: GuildMetrics):
        r = await self.__request("POST", "/stats", data=metrics.dict())
        print(r)
