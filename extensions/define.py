import lightbulb
import hikari
import re
import json

from utils.data import terms_dict
from typing import Sequence, Union

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("define")

REGEX_PATTERN = re.compile(r"<\$cc[^>]*>|<@cc[^>]*>|<\$ba[^>]*>|<\/>")


@plugin.command
@lightbulb.option("term", "In-game term", required=True, autocomplete=True)
@lightbulb.command(
    "define", "Get the in-game definition of an in-game term", auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def define(ctx):
    term = ctx.options.term.lower()

    for _, term_dict in terms_dict.items():
        if term_dict.get("termName", "").lower() == term:
            em = hikari.Embed(
                title=term_dict.get("termName"),
                description=f"{re.sub(REGEX_PATTERN, ' **', term_dict.get('description'))}",
            )
            await ctx.respond(em)
            return

    await ctx.respond(hikari.Embed(description=f"Term {term} not found."))


@define.autocomplete("term")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_terms = [
        term_dict.get("termName")
        for _, term_dict in terms_dict.items()
        if user_input.lower() in term_dict.get("termName").lower()
    ]
    matching_terms = matching_terms[:25]
    return [hikari.CommandChoice(name=term, value=term) for term in matching_terms]


def load(bot):
    bot.add_plugin(plugin)
