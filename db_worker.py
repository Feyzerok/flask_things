from peewee import *

db = SqliteDatabase('data/em_resources.db')

class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db