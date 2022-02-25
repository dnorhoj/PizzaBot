from typing import List, TypedDict


BasketItem = TypedDict('Basket', {
    'name': str,
    'price': int
})

Basket = List(BasketItem)

User = TypedDict('User', {
    'discord_id': int,
    'name': str,
    'basket': Basket
})