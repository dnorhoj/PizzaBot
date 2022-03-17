from nextcord import ButtonStyle, Color, Embed, Interaction, ui

from config import MENU


class BestilButton(ui.Button):
    def __init__(self, *, label: str, buttonstyle: ButtonStyle, bestilview: 'BestilView', price: int):
        self.bestilview = bestilview
        self.res = label

        super().__init__(
            label=f"{label} ({price} kr.)",
            style=buttonstyle
        )

    async def callback(self, interaction: Interaction):
        await self.bestilview.end(interaction, self.res)


class BestilView(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

        for pizz in MENU[0]["items"]:
            self.add_item(
                BestilButton(
                    label=pizz["name"],
                    price=pizz["price"],
                    buttonstyle=pizz["style"],
                    bestilview=self
                )
            )

    @ui.button(label='Cancel', style=ButtonStyle.red)  # Cancel interaction
    async def farvel(self, _, interaction: Interaction):
        await self.end(interaction)

    async def end(self, interaction: Interaction, value: str = None):
        self.value = value
        
        embed = Embed(
            title="La Sosta farvel",
            description=f"+{value}",
            color=Color.red()
        )

        if value is None:
            embed.description = ""

        await interaction.response.edit_message(embed=embed, content=None, view=None)
        self.stop()
