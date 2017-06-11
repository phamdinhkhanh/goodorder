from flask_restful import Resource, reqparse
from model.good import *
from model.customer import Customer
import mlab
from model.order import Order, SingleOrder


class OrderRes(Resource):
    def get(self):
        orders = Order.objects()
        return mlab.list2json(orders)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="items", type=list, location="json")
        parser.add_argument(name="user_id", type=str, location="json")
        #parser.add_argument(name="id", type= int, location="json")
        #parser.add_argument(name="count", type=int, location="json")

        body = parser.parse_args()
        items = body["items"]
        user_id = body.user_id
        total_spend = 0
        order_item = []
        for item in items:
           good_id = item["id"]
           count = item["count"]
           good = Good.objects().with_id(good_id)
           price = good.price
           print("good_id:", good_id,";count: ",count,"price: ",price)
           total_spend += price*count
           singleOrder = SingleOrder(good = good, count = count)
           order_item.append(singleOrder)
        customer = Customer.objects().with_id(user_id)
        #print(mlab.item2json(order_item[0]))
        #print("order_item0:",mlab.item2json(order_item[0]),"order_item1:",order_item[1])
        order = Order(items = order_item,customer = customer,
                      totalspend = total_spend)
        order.save()
        add_order = Order.objects().with_id(order.id)
        return mlab.item2json(add_order)







