from disnake.ext.commands.cog import Cog
from disnake.ext.commands.slash_core import slash_command
from disnake import Embed
from humanize import intword, naturaltime
from disnake.ext.commands.params import Param
from disnake.interactions import ApplicationCommandInteraction
from ..obyn import Obyn


class Summary(Cog):
    def __init__(self, bot: Obyn):
        self.bot = bot
        self.post_metrics.start()

    @slash_command(
        name="summary", description="summarizes", guild_ids=[846429112608620616]
    )
    async def summary(
        self,
        ctx: ApplicationCommandInteraction,
        time: int = Param(default=1, le=90, ge=1, description="amount of time to summarize (default, 1)"),
        unit: str = Param(default="days", choices=("hours", "days", "weeks", "months"), description="time unit (default, days)")
    ):
        if not ctx.guild_id:  # actually shut up mypy
            return

        time_dict = {"hours": 3600, "days": 86400, "weeks": 604800, "months": 2592000}
        seconds = time * time_dict[unit]
        metrics = await self.bot.get_metrics(ctx.guild_id, time, unit)

        em = Embed(
            title="Summary",
            description=f"There were {intword(ac := metrics.total_events)} events in total from {naturaltime(seconds)} to today",
            color=0x2F3136,
        )
        em.add_field(
            "Stats",
            f"""
        - **{metrics.bans+metrics.kicks+metrics.timeouts}** total moderation actions
        - **{intword(ac - (metrics.bans + metrics.kicks + metrics.timeouts))}** other events
        """,
        )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Summary(bot))
