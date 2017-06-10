from mongoengine import *
import mlab


class Good(Document):
    goodname = StringField()
    price = FloatField()


