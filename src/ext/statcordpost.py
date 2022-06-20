from disnake.ext.commands.cog import Cog
from statcord import StatcordClient


class MyStatcordCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statcord_client = StatcordClient(bot, bot.statcord_token)

    def cog_unload(self):
        self.statcord_client.close()


def setup(bot):
    bot.add_cog(MyStatcordCog(bot))
