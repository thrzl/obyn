from src.obyn import Obyn
from disnake.interactions import ApplicationCommandInteraction
from asteval import Interpreter

bot = Obyn()


@bot.slash_command(name="eval")
async def eval_(ctx: ApplicationCommandInteraction, *, command: str):
    if ctx.author.id != 536644802595520534:
        return await ctx.send("You are not allowed to use this command.")
    aeval = Interpreter()
    aeval.symtable["bot"] = bot
    aeval.symtable["ctx"] = ctx
    aeval.symtable["channel"] = ctx.channel
    ctx.channel.get_partial_message(123)
    res = aeval(command)
    await ctx.send(res or "complete")


@bot.slash_command(name="reload")
async def reload_(ctx: ApplicationCommandInteraction, *, module: str = ""):
    if ctx.author.id != 536644802595520534:
        return await ctx.send("You are not allowed to use this command.")
    if module == "":
        for i in bot.cogs:
            bot.unload_extension(i)
    else:
        # m = module.capitalize()
        bot.unload_extension(module)
    bot.load_extensions("src/ext")
    await ctx.send("Reloaded")


bot.load_extensions("src/ext")
bot.run()
