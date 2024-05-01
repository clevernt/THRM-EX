import lightbulb
import hikari
import requests
import re

from typing import Sequence, Union

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("define")

terms = requests.get("https://awedtan.ca/api/define").json()
REGEX_PATTERN = re.compile(r"<\$cc[^>]*>|<@cc[^>]*>|<\/>")


@plugin.command
@lightbulb.option("term", "In-game term", required=True, autocomplete=True)
@lightbulb.command(
    "define", "Get the in-game definition of an in-game term", auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def define(ctx):
    term = ctx.options.term
    resp = requests.get(f"https://awedtan.ca/api/define/{term.lower()}")
    if resp.status_code != 200:
        await ctx.respond(hikari.Embed(description=f"Term `{term}` not found."))
        return

    definition = resp.json()
    em = hikari.Embed(
        title=definition.get("value").get("termName"),
        description=f"{re.sub(REGEX_PATTERN, '**', definition.get('value').get('description'))}",
    )

    await ctx.respond(em)


@define.autocomplete("term")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_terms = [
        term["value"]["termName"]
        for term in terms
        if user_input in term["value"]["termName"].lower()
    ]
    matching_terms = matching_terms[:25]
    return [hikari.CommandChoice(name=term, value=term) for term in matching_terms]


def load(bot):
    bot.add_plugin(plugin)
