from os import environ

from nextcord import Interaction, SlashOption, Color, Embed
from nextcord.ext import commands

from ui import BestilView

bot = commands.Bot(command_prefix="pb!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(guild_ids=[451418956436209684])
async def bestil(
    interaction: Interaction,
    custom:str = SlashOption(
        name="custom",
        required=False
    )
):
    if not custom is None:
        embed = Embed(
            title="La Sosta farvel",
            description=f"+{custom}",
            color=Color.red()
        )
        
        await interaction.response.send_message(embed=embed)
        print(custom)
        return

    bestilview = BestilView()
    await interaction.response.send_message(
        "La sosta goddag. Hvad skal du ha'?",
        ephemeral=True,
        view=bestilview
    )

    await bestilview.wait()

    print(bestilview.value)

bot.run(environ["DISCORD_TOKEN"])
