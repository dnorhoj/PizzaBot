from os import environ

import peewee

#db = peewee.SqliteDatabase('pizza.db')
db = peewee.PostgresqlDatabase(environ['POSTGRES_DB'], user=environ['POSTGRES_USER'], password=environ['POSTGRES_PASSWORD'],
                               host=environ['POSTGRES_HOST'], port=environ['POSTGRES_PORT'], autorollback=True)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    discord_id = peewee.CharField(unique=True)
    name = peewee.CharField()
    phoneno = peewee.CharField()


class Order(BaseModel):
    created = peewee.DateTimeField()
    created_by = peewee.ForeignKeyField(User, backref='created_by')
    order_message = peewee.CharField()
    open = peewee.BooleanField(default=True)


class BasketItem(BaseModel):
    item = peewee.CharField()
    added_by = peewee.ForeignKeyField(User, backref='added_by')
    order = peewee.ForeignKeyField(Order, backref='order')


def create_tables():
    with db:
        db.create_tables([User, Order, BasketItem])


if __name__ == '__main__':
    create_tables()
