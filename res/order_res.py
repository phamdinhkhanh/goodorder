from flask_restful import Resource, reqparse
from model.good import *
from model.customer import Customer
import mlab
from model.order import Order, SingleOrder
import json
import re
parser = reqparse.RequestParser()
parser.add_argument(name="items", location="json", action = "append")
parser.add_argument(name="user_id", type=str, location="json")

class OrderRes(Resource):
    def get(self):
        orders = Order.objects()
        return mlab.list2json(orders)

    def post(self):

        #parser.add_argument(name="id", type= int, location="json")
        #parser.add_argument(name="count", type=int, location="json")

        body = parser.parse_args()
        items = body["items"]
        user_id = body.user_id
        total_spend = 0
        order_item = []
        dumps = json.dumps(items)
        ldumps = re.findall(r"[\w']+",dumps)
        print(len(items))
        for i in range(0,len(items)):
            good_id = ldumps[4*i+1][1:-1]
            count = int(ldumps[4*i+3])
            good = Good.objects().with_id(good_id)
            price = good.price
            total_spend += price*count
            singleOrder = SingleOrder(good = good, count = count)
            order_item.append(singleOrder)
        print("order_item:",mlab.list2json(order_item))
        customer = Customer.objects().with_id(user_id)
        order = Order(items = order_item,customer = customer,
                      totalspend = total_spend)
        order.save()
        add_order = Order.objects().with_id(order.id)
        return mlab.item2json(add_order)







