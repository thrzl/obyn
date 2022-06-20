from disnake.ext.commands.bot import InteractionBot
from disnake.interactions import ApplicationCommandInteraction
from disnake import AuditLogAction, Member

from .db import GuildMetrics, SupaClient
from dotenv import load_dotenv
from os import environ

from cachetools import cached, TTLCache

load_dotenv()


class Obyn(InteractionBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = SupaClient(environ["SUPABASE_URL"], environ["SUPABASE_KEY"])
        self.statcord_token = environ["STATCORD_KEY"]
        self._important_events = (
            AuditLogAction.kick,
            AuditLogAction.ban,
            AuditLogAction.member_prune,
        )

    @cached(cache=TTLCache(maxsize=500, ttl=43200))  # 12 hours
    async def get_metrics(self, guild_id: int, time: int = 1, unit: str = "days"):
        guild = self.get_guild(guild_id)
        time_dict = {"hours": 3600, "days": 86400, "weeks": 604800, "months": 2592000}
        seconds = time * time_dict[unit]
        all_actions = tuple(await (guild.audit_logs(limit=None, after=(datetime.utcnow() - timedelta(seconds=seconds))).flatten()))  # type: ignore
        bans = len(
            tuple(filter(lambda event: event.action == AuditLogAction.ban, all_actions))
        )
        kicks = len(
            tuple(
                filter(lambda event: event.action == AuditLogAction.kick, all_actions)
            )
        )
        timeouts = len(
            tuple(
                filter(
                    lambda event: event.action == AuditLogAction.member_update
                    and event.target._communication_disabled_until
                    if type(event.target) == Member
                    else False,
                    all_actions,
                )
            )
        )
        return GuildMetrics(
            guild_id=guild_id,
            members=guild.members,
            bans=bans,
            kicks=kicks,
            total_events=len(all_actions),
            timeouts=timeouts,
        )

    async def on_ready(self):
        print("FEEL NATURE'S WRATH")

    def run(self):
        super().run(token=environ["DISCORD_TOKEN"])

    async def on_application_command(self, interaction: ApplicationCommandInteraction):
        return await super().on_application_command(interaction)
