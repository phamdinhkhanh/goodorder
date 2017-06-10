from flask_restful import Resource, reqparse
import mlab
from model.good import *

class GoodRes(Resource):
    def get(self):
        good =  Good.objects()
        return mlab.list2json(good), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="price", type=float, location="json")

        body = parser.parse_args()
        name = body.name
        price = body.price

        good = Good(goodname=name, price=price)
        good.save()
        print("saved")
        add_good = Good.objects().with_id(good.id)
        return mlab.item2json(add_good), 200






