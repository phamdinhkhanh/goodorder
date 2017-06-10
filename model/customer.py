from mongoengine import *
import mlab
from model.customer import *


class Customer(Document):
    username = StringField()
    password = StringField()

