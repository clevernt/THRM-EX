import lightbulb
import hikari
import os
import miru

from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    help_slash_command=True,
)
bot.d.miru = miru.Client(bot)


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            hikari.Embed(description="something went wrong, blame dest")
        )
        raise event.exception


@bot.command()
@lightbulb.command("ping", "Check bot's ping", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    embed = hikari.Embed(
        title="Pong!", description=f"**{bot.heartbeat_latency * 1_000:.0f}ms**"
    )
    await ctx.respond(embed)


bot.load_extensions_from("extensions")
bot.run()
