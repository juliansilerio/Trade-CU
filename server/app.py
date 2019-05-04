from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Order
import generate_entities as ge

# ORDERS = [
#     {
#         'side' : 'B',
#         'ticker' : 'COMSW3134-001',
#         'class' : 'Data structures',
#         'time' : 'MW 8:10',
#         'professor' : 'Dunce',
#         'price' : '2',
#     },
#     {
#         'side' : 'S',
#         'ticker' : 'COMSW4491-002',
#         'class' : 'Machine learning for dummies',
#         'time' : 'TR 6:10',
#         'professor' : 'Beevis',
#         'price' : '1',
#     },
#     {
#         'side' : 'S',
#         'ticker' : 'COMSW4111-007',
#         'class' : 'Databases',
#         'time' : 'MWF 1:10',
#         'professor' : 'Oak',
#         'price' : '2',
#     }
# ]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.app=app
db.init_app(app)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/orders', methods=['GET', 'POST'])
def all_orders():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        ORDERS.append({
            'side' : post_data.get('side'),
            'ticker' : post_data.get('ticker'),
            'class' : post_data.get('class'),
            'time' : post_data.get('time'),
            'professor' : post_data.get('professor'),
            'price' : post_data.get('price'),
        })
        response_object['message'] = 'Order created'
    else:
        orders = Order.query.all()
        ORDERS=[]
        for o in orders:
            ORDERS.append({
                'side' : o.side,
                'ticker' :  '{}{}-{}'.format(o.course.dept_short, o.course.number, str(o.course.section).zfill(3)),
                'class' : str(o.course.title),
                'time' : str(o.course.day) + " " +  str(o.course.time),
                'professor' : o.course.faculty,
                'price' : o.price
            })
        response_object['orders'] = ORDERS
    return jsonify(response_object)

@app.route('/users', methods=['GET'])
def all_users():
    from models import User
    users = ''
    for user in User.query.all():
        users += '<p>{}</p>'.format(user.uni)
    return '%s' % users

'''
User CRUD functions
'''
def create_user():
    pass

def update_user():
    pass

def view_user():
    pass

def delete_user():
    pass

'''
Order CRUD functions
'''
def create_order():
    pass

def update_order():
    pass

def view_order():
    pass

def delete_order():
    pass

'''
Course CRUD functions
'''
def create_course():
    pass

def update_course():
    pass

def view_course():
    pass

def delete_course():
    pass

if __name__ == '__main__':
    app.run()
