from disnake.ext.commands.cog import Cog
from ..obyn import Obyn
from disnake import Embed
from disnake.ext.tasks import loop
from humanize import intword


class Tasks(Cog):
    def __init__(self, bot: Obyn):
        self.bot = bot
        self.post_metrics.start()

    @loop(hours=24)
    async def post_metrics(self):
        for guild in self.bot.guilds:
            metrics = await self.bot.get_metrics(guild.id)
            await self.bot.db.send_metrics(guild.id, metrics)
            print(f"sent metrics for guild {guild.id}")

    @post_metrics.before_loop
    async def before_post_metrics(self):
        print("Starting metrics posting loop")
        await self.bot.wait_until_ready()

    @loop(hours=24)
    async def log_metrics(self):
        for guild in self.bot.guilds:
            metrics = await self.bot.get_metrics(guild.id)
            em = Embed(
                title="Summary",
                description=f"There were {intword(ac := metrics.total_events)} events in total in the past day",
                color=0x2F3136,
            )
            em.add_field(
                "Stats",
                f"""
            - **{metrics.bans+metrics.kicks+metrics.timeouts}** total moderation actions
            - **{intword(ac - (metrics.bans + metrics.kicks + metrics.timeouts))}** other events
            """,
            )


def setup(bot):
    bot.add_cog(Tasks(bot))
