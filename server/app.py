from flask import Flask, jsonify, request, render_template
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

@app.route('/addOrder', methods=['POST'])
def addOrder():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    course = Course.query.get(post_data.get('course'))
    student = User.query.get(post_data.get('user')['uni'])
    side=post_data.get('side')
    if (side == 'SELL' and Seat.query.filter_by(student=student,course=course).first()) or side == 'BUY':
        order = Order(course=course, student=student, price=post_data.get('price'), side=side)
        db.session.add(order)
        db.session.commit()
        response_object['message'] = 'Order created'
    else:
        response_object['message'] = 'Invalid order, no position in course'

    print(response_object['message'])
    return jsonify(response_object)

@app.route('/getOrders', methods=['POST'])
def get_orders():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    student = User.query.get(post_data.get('user')['uni'])
    orders = Order.query.all()
    ORDERS= []
    myORDERS = []
    for o in orders:
        res_o = {
            'side' : o.side,
            'ticker' :  '{}{}-{}'.format(o.course.dept_short, o.course.number, str(o.course.section).zfill(3)),
            'class' : str(o.course.title),
            'time' : str(o.course.day) + " " +  str(o.course.time),
            'professor' : o.course.faculty,
            'price' : o.price,
            'id' : o.id,
        }
        if o.student == student:
            myORDERS.append(res_o)
        else:
            ORDERS.append(res_o)
    response_object['orders'] = ORDERS
    response_object['myOrders'] = myORDERS

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

    seller = o.student # order placer
    buyer = user # you're executing their sell order
    if o.side == 'BUY':
        seller = user #you're executing their buy order
        buyer = o.student # order placer

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

@app.route('/delete', methods=['PUT'])
def delete():
    response_object = {'status': 'success'}
    response_object['message'] = 'Order could not be deleted '
    put_data = request.get_json()
    o = Order.query.get(put_data.get('order'))
    user = User.query.get(put_data.get('user')['uni'])


    if o.student == user:
        Order.query.filter_by(id=put_data.get('order')).delete()
        db.session.commit()
        response_object['message'] = 'Order deleted'
    else:
        response_object['message'] +=' {} {} {} {}'.format(o.side, o.price, o.course, o.student)
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

@app.route('/see_orders')
def see_orders():
    users = User.query.all()
    print([user.orders for user in users])
    return render_template('see_orders.html', users=users)

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
