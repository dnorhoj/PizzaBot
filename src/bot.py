import re
from collections import Counter
from datetime import datetime
from os import environ
from random import choice
from string import ascii_lowercase

import peewee
from nextcord import errors, Color, Embed, Interaction, SlashOption
from nextcord.ext import commands

import models
from config import ADMINS, GUILD_IDS, INFO, VOICE_LINES, PING_ID
from ui import BestilView
from models import create_tables

create_tables()

bot = commands.Bot(command_prefix=''.join(
    [choice(ascii_lowercase) for _ in range(32)]))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def render_embed(order: models.Order, interaction: Interaction, closed=False):
    items = (models.BasketItem
             .select(models.BasketItem, models.Order)
             .join(models.Order)
             .where(models.BasketItem.order.id == order.id)
             .execute())

    if closed:
        embed = Embed(title=f"[CLOSED] Order #{order.id}", color=Color.red())
    else:
        embed = Embed(title=f"Order #{order.id}", color=Color.green())

    counts = Counter(map(lambda item: item.item, items))
    lines = [f"{counts[i]}x {i}" for i in counts]
    value = "\n".join(lines)
    if len(value) == 0:
        value = "Ingen bestilling endnu"
    elif len(value) >= 1024:
        value = value[:1016]+"\n**...**"

    embed.add_field(name="Bestilling", value=value)

    embed.add_field(
        name="Info", value=f"Started by <@{order.created_by.discord_id}>\n"+INFO)

    try:
        orig_message = await interaction.channel.fetch_message(order.order_message)
        await orig_message.edit(embed=embed)
        
    except errors.NotFound:
        pass

@bot.slash_command(
    guild_ids=GUILD_IDS,
    description="This command opens a new order if one does not already exist"
)
async def start(interaction: Interaction):
    order = models.Order.get_or_none(models.Order.open == True)
    if order is not None:
        await interaction.send(f"There is already an order open started by <@{order.created_by.discord_id}>", ephemeral=True)
    else:
        try:
            user = models.User.get(
                models.User.discord_id == interaction.user.id)
        except models.User.DoesNotExist:
            return await interaction.send("Please set your name with `/register`!", ephemeral=True)

        msg = await interaction.channel.send(f"<@&{PING_ID}>")

        try:
            order = models.Order.create(
                created=datetime.now(), created_by=user, open=True, order_message=msg.id)
            await render_embed(order, interaction)
            await msg.pin()
            await interaction.send("Order created!", ephemeral=True)
        except:
            await interaction.send("Unknown error. Please contact an admin...", ephemeral=True)
            raise


@bot.slash_command(
    guild_ids=GUILD_IDS,
    description="Closes the current order. Can only be run by the person who started the order."
)
async def close(interaction: Interaction):
    current_order = models.Order.get_or_none(models.Order.open == True)

    if current_order is None:
        return await interaction.send("There is no open order...", ephemeral=True)

    if interaction.user.id not in ADMINS and current_order.created_by.discord_id != str(interaction.user.id):
        return await interaction.send("You did not start the order.", ephemeral=True)

    # User started the order.
    try:
        models.Order.update({models.Order.open: False}).where(
            models.Order.id == current_order.id).execute()
    except:
        await interaction.send("Unknown error!", ephemeral=True)
        raise

    await render_embed(current_order, interaction, True)
    await interaction.send("Order is now closed!")


@bot.slash_command(
    guild_ids=GUILD_IDS,
    description="Order with this command."
)
async def order(
    interaction: Interaction,
    custom: str = SlashOption(
        name="custom",
        required=False
    )
):
    try:
        user = models.User.get(models.User.discord_id == interaction.user.id)
    except models.User.DoesNotExist:
        return await interaction.send("Please set your name with `/register`!", ephemeral=True)

    try:
        order = models.Order.get(models.Order.open == True)
    except:
        return await interaction.send("No order has been started... Start one with `/start`", ephemeral=True)

    res = ""
    if custom is not None:
        if len(custom) > 100:
            return await interaction.send("Item name can only be 100 characters long...", ephemeral=True)
        custom = custom.capitalize()
        embed = Embed(
            title="La Sosta farvel",
            description=f"+{custom}",
            color=Color.red()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        res = custom
    else:
        bestilview = BestilView()
        await interaction.response.send_message(
            choice(VOICE_LINES),
            ephemeral=True,
            view=bestilview
        )

        await bestilview.wait()
        res = bestilview.value

    if res is not None:
        try:
            models.BasketItem.create(added_by=user, item=res, order=order)
            await render_embed(order, interaction)
        except:
            await interaction.send("Unknown error!", ephemeral=True)
            raise


@bot.slash_command(
    guild_ids=GUILD_IDS,
    description="Set your name for ordering"
)
async def register(
    interaction: Interaction,
    name: str = SlashOption(
        name="name",
        required=True,
        description="Please insert your own name to facilitate the ordering."
    ),
    phoneno: str = SlashOption(
        name="phonenumber",
        required=True,
        description="Please insert your phone number to facilitate the ordering,"
    )
):
    if re.match(r'^[0-9]{8}$', phoneno) is None:
        return await interaction.send("Please use the following format: `12345678`", ephemeral=True)

    try:
        models.User.create(
            discord_id=interaction.user.id, name=name.capitalize(), phoneno=phoneno)
    except peewee.PeeweeException:
        return await interaction.send("You are already registered.", ephemeral=True)

    await interaction.send(f"Done", ephemeral=True)


@bot.slash_command(
    guild_ids=GUILD_IDS,
    description="See your basket"
)
async def basket(interaction: Interaction):
    try:
        order = models.Order.get(models.Order.open == True)
    except:
        return await interaction.send("No order has been started... Start one with `/start`", ephemeral=True)

    items = (models.BasketItem
             .select(models.BasketItem.item)
             .join_from(models.BasketItem, models.User)
             .join_from(models.BasketItem, models.Order)
             .where(models.BasketItem.added_by.discord_id == interaction.user.id)
             .where(models.BasketItem.order.id == order.id)
             .execute())

    counts = Counter(map(lambda item: item.item, items))
    lines = [f"{counts[i]}x {i}" for i in counts]
    if len(lines) == 0:
        lines = ["Ingen bestilling endnu"]

    embed = Embed(title=f"Your order", color=Color.green(),
                  description="\n".join(lines))

    embed.set_footer(text="Clear basket with /clearbasket")

    await interaction.send(embed=embed, ephemeral=True)


@bot.slash_command(
    guild_ids=GUILD_IDS,
    description="Clear your basket"
)
async def clearbasket(interaction: Interaction):
    try:
        order = models.Order.get(models.Order.open == True)
    except:
        return await interaction.send("No order has been started... Start one with `/start`", ephemeral=True)

    basket = (models.BasketItem
              .select(models.BasketItem.id)
              .join_from(models.BasketItem, models.User)
              .join_from(models.BasketItem, models.Order)
              .where(models.BasketItem.added_by.discord_id == interaction.user.id)
              .where(models.BasketItem.order.id == order.id))

    (models.BasketItem
     .delete()
     .where(models.BasketItem.id.in_(basket))
     .execute())

    await render_embed(order, interaction)
    await interaction.send("Cleared your basket!", ephemeral=True)


@bot.slash_command(
    guild_ids=GUILD_IDS,
    description="Get payment info",
)
async def payments(
    interaction: Interaction,
    order_number: int = SlashOption(
        name="order_number",
        required=False,
        description="Optional: Order number"
    )
):
    if order_number:
        order = models.Order.get_or_none(models.Order.id == order_number)
        if order is None:
            return await interaction.send("Order does not exist!", ephemeral=True)
    else:
        order = (models.Order
                 .select()
                 .order_by(models.Order.created.desc())
                 .first())

    all_items = (models.BasketItem
                 .select()
                 .join_from(models.BasketItem, models.User)
                 .join_from(models.BasketItem, models.Order)
                 .where(models.BasketItem.order.id == order.id)
                 .execute())

    baskets = {}
    for item in all_items:
        new = baskets.get(item.added_by.id, [item.added_by.name])
        new.append(item.item)
        baskets[item.added_by.id] = new

    embed = Embed(title=f"Order #{order.id}",
                  description="Payment information",
                  color=Color.green())
    
    ordertext = []
    for userid in baskets:
        ordertext.append(f"**{baskets[userid][0]}**")
        for item in baskets[userid][1:]:
            ordertext[-1] += f"\n`{item}`"
    
    ordertext = "\n\n".join(ordertext)
    
    if len(ordertext) == 0:
        ordertext = "Empty order"

    embed.add_field(
        name="Orders",
        value=ordertext,
        inline=True
    )

    embed.set_footer(text="Started at:")
    embed.timestamp = order.created

    await interaction.send(embed=embed, ephemeral=True)


bot.run(environ["DISCORD_TOKEN"])
