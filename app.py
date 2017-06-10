from flask import Flask
import mlab
from flask_restful import Resource, Api

from res.good_res import GoodRes
from res.login import jwt_init,RegisterRes
from res.order_res import OrderRes

mlab.connect()

app = Flask(__name__)
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')

api = Api(app)
jwt = jwt_init(app)


api.add_resource(RegisterRes,"/api/register")
api.add_resource(OrderRes, "/api/order")
api.add_resource(GoodRes,"/api/good")

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()
