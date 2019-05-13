from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager
from models import db, Order, User, Course, Seat
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

@app.route('/courses', methods=['GET'])
def all_courses():
    response_object = {'status': 'success'}
    courses = Course.query.all()
    courses_res = []
    courses_res.append({ 'value': 'null', 'text': 'Please select an option' })
    for course in courses:
        courses_res.append({ 'value': course.call, 'text': str(course)[1:-1]})
    response_object['courses'] = courses_res
    return jsonify(response_object)

@app.route('/orders', methods=['GET', 'POST'])
def all_orders():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        course = Course.query.get(post_data.get('course'))
        student = User.query.get(post_data.get('user'))
        side=post_data.get('side')
        if (side == 'SELL' and Seat.query.filter_by(student=student,course=course).first()) or side == 'BUY':
            order = Order(course=course, student=student, price=post_data.get('price'), side=side)
            db.session.add(order)
            db.session.commit()
            response_object['message'] = 'Order created'
        else:
            response_object['message'] = 'Invalid order, no position in course'

        print(response_object['message'])
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
                'price' : o.price,
                'id' : o.id,
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

@app.route('/execute', methods=['PUT'])
def execute():
    response_object = {'status': 'success'}
    response_object['message'] = 'Order failed to execute'
    put_data = request.get_json()
    o = Order.query.get(put_data.get('order'))
    user = User.query.get(put_data.get('user')['uni'])

    seller = o.student
    buyer = user # you're executing the buy order
    if o.side == 'SELL':
        seller = user #you're executing the sell order
        buyer = o.student

    seat = Seat.query.filter_by(student=seller,course=o.course).first()
    if seat and buyer.credits >= o.price and seller != buyer:
        buyer.credits -= o.price
        seller.credits += o.price
        seat.student = buyer

        Order.query.filter_by(id=put_data.get('order')).delete()
        db.session.add(buyer)
        db.session.add(seller)
        db.session.add(seat)
        db.session.commit()
        response_object['message'] = 'Order executed'
    else:
        response_object['message'] +=' {} {} {} {} {}'.format(buyer, buyer.credits, o.price, seller.credits, seller)
    return jsonify(response_object)


@app.route('/check_user', methods=['POST'])
def login():
    response_object = { 'status' : 'success' }
    post_data = request.get_json()
    user = User.query.get(post_data.get('username'))
    print(user)
    if user != None:
        response_object['authenticated'] = 'true'
        this_user = {
            'uni': user.uni,
            'credits' : user.credits
        }
        response_object['user'] = this_user
    return jsonify(response_object)

@app.route('/user', methods=['GET', 'POST'])
def user():
    response_object = { 'status' : 'success' }
    post_data = request.get_json()
    print(post_data)
    user = User.query.get(post_data.get('user'))
    USER_res = {
        'uni': user.uni,
        'credits' : user.credits
    }
    response_object['user'] = USER_res
    print(USER_res)
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
