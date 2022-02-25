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
                "name": "Pep m. dres",
                "style": ButtonStyle.green,
                "price": 57
            },
            {
                "name": "Pep u. dres",
                "style": ButtonStyle.green,
                "price": 50
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