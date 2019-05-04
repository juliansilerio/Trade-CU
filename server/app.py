from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager
from models import db, Order, User
import generate_entities as ge

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.app=app
db.init_app(app)

# login config
login_manager = LoginManager()
login_manager.init_app(app)

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

@app.route('/check_user', methods=['POST'])
def login():
    response_object = { 'status' : 'success' }
    post_data = request.get_json()
    user = User.query.get(post_data.get('username'))
    if user != None:
        response_object['authenticated'] = 'true'
    return jsonify(response_object)

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

@login_manager.user_loader
def load_user(uni):
    return User.query.get(uni)


if __name__ == '__main__':
    app.run()
