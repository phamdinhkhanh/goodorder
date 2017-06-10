from mongoengine import *
from model.good import Good
import mlab
from model.customer import *


class SingleOrder(EmbeddedDocument):
    good = ReferenceField("Good")
    count = IntField()

    def get_json(self):
        return {
            "good":Good.objects().with_id(self.good.id).get_json(),
            "count":self.count
        }

class Order(Document):
    items = ListField(EmbeddedDocumentField("SingleOrder"))
    customer = ReferenceField("Customer")
    totalspend = FloatField()
