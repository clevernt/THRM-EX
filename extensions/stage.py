import hikari
import lightbulb
import requests

from utils import get_enemies

plugin = lightbulb.Plugin("stage")


def get_stage_image(stage_code, mode):
    stage_mode = "toughstage" if mode.lower() == "challenge" else "stage"
    resp = requests.get(
        f"https://hellabotapi.cyclic.app/{stage_mode}/{stage_code}?include=excel.stageId"
    )
    data = resp.json()
    stage_id = data["value"][0]["excel"]["stageId"].rstrip("#f#")

    return f"https://raw.githubusercontent.com/yuanyan3060/ArknightsGameResource/main/map/{stage_id}.png"


@plugin.command
@lightbulb.option("stage_code", "Stage Code", required=True)
@lightbulb.option(
    "mode",
    "Stage Mode (affects stages that have a different layout in Adverse)",
    choices=["Normal", "Challenge"],
    default="Normal",
)
@lightbulb.command("stage", "Get information about a stage", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def stage(ctx):
    stage_code = ctx.options.stage_code
    mode = ctx.options.mode
    enemies_data = await get_enemies(stage_code, mode)
    if not enemies_data:
        await ctx.respond(
            hikari.Embed(
                title=f"Error fetching enemies for stage `{stage_code}` `{mode}`",
                description="If you searched for Challenge mode, try searching in Normal Mode.",
            )
        )
        return

    em = hikari.Embed(
        title=f"{stage_code} - {mode.title()}",
        description="Use </enemy:1212563798804926525> for more details about an enemy",
        color="#FFFFFF",
    )
    em.set_image(get_stage_image(stage_code, mode))
    for enemy in enemies_data:
        em.add_field(
            f'{enemy["name"]} - {enemy["status"]}',
            f'Level: {enemy["level"]} | ATK: {enemy["stats"]["ATK"]} | DEF: {enemy["stats"]["DEF"]} | RES: {enemy["stats"]["RES"]}',
        )

    await ctx.respond(em)


def load(bot):
    bot.add_plugin(plugin)
