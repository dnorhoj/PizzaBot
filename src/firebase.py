import types
from typing import Union

import pyrebase
from creds import FIREBASE

firebase = pyrebase.initialize_app(FIREBASE).database() # Create firebase object
db = firebase.database() # Create database object

def create_user(userid: int, name: str) -> types.Users:
    # Raise exception if user already exists for id
    pass

def get_user(userid: int) -> Union[types.User, None]:
    # Return None if user does not exist
    pass
 
def add_to_basket(userid: int, itemname: str, price: int) -> types.Basket:
    pass

def get_basket(userid: int) -> types.Basket:
    pass

def clear_basket(userid: int) -> None:
    pass
