from nextcord import ButtonStyle

MENU = [
    {
        "type": "Pizza",
        "items": [
            {
                "name": "Salatpizza",
                "style": ButtonStyle.green,
                "price": 50
            },
            {
                "name": "Pep",
                "style": ButtonStyle.green,
                "price": 50
            },
            {
                "name": "Pep m. dres",
                "style": ButtonStyle.green,
                "price": 57
            },
            {
                "name": "Fiskefilet",
                "style": ButtonStyle.blurple,
                "price": 57
            }
        ]
    }
]

VOICE_LINES = [
    "La Sosta goddag.",
    "La Sosta goddag, hva' skal du ha'?",
    "La Sosta?",
    "EOW DIG HVAD SKAL DU HAVE?",
    "Beep, Boop, bestil."
]

GUILD_IDS = [451418956436209684,764063369123725324]
PING_ID = 940654339079430254

ADMINS = [
    281409966579908608,
    305246941992976386,
]

INFO = """Order with `/order`
View your basket with `/basket`
See your basket with `WIP`
Close the order with `/order`
"""