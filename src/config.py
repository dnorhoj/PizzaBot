from nextcord import ButtonStyle

MENU = [
    {
        "type": "Pizza",
        "items": [
            {
                "name": "Salatpizza",
                "style": ButtonStyle.green,
                "price": 56
            },
            {
                "name": "Pep",
                "style": ButtonStyle.green,
                "price": 56
            },
            {
                "name": "Pep m. dres",
                "style": ButtonStyle.green,
                "price": 63
            },
            {
                "name": "Durum Shawarma",
                "style": ButtonStyle.green,
                "price": 62
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

GUILD_IDS = [451418956436209684, 764063369123725324]
PING_ID = 940654339079430254

ADMINS = [
    281409966579908608,
    305246941992976386,
]

INFO = """Order with `/order`
View your basket with `/basket`
Clear your basket with `/clearbasket`
Close the order with `/close`
See who ordered what with `/payment`
"""
