import lightbulb
import hikari
import os

from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    help_slash_command=True,
)


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            hikari.Embed(description="something went wrong, blame dest")
        )
        raise event.exception


bot.load_extensions_from("extensions")
bot.run()
