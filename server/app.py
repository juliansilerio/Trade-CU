from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db


ORDERS = [
    {
        'side' : 'B',
        'ticker' : 'COMSW3134-001',
        'class' : 'Data structures',
        'time' : 'MW 8:10',
        'professor' : 'Dunce',
        'price' : '2',
    },
    {
        'side' : 'S',
        'ticker' : 'COMSW4491-002',
        'class' : 'Machine learning for dummies',
        'time' : 'TR 6:10',
        'professor' : 'Beevis',
        'price' : '1',
    },
    {
        'side' : 'S',
        'ticker' : 'COMSW4111-007',
        'class' : 'Databases',
        'time' : 'MWF 1:10',
        'professor' : 'Oak',
        'price' : '2',
    }
]

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
        response_object['orders'] = ORDERS
    return jsonify(response_object)

@app.route('/users', methods=['GET'])
def all_users():
    from models import User
    users = ''
    for user in User.query.all():
        users += '<p>{}</p>'.format(user.uni)
    return '%s' % users

if __name__ == '__main__':
    app.run()
