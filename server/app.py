from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
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

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

'''
COURSE FUNCTIONS
'''
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

'''
SEAT FUNCTIONS
'''
@app.route('/mySeats', methods=['POST'])
def my_seats():
    response_object = { 'status': 'success' }
    post_data = request.get_json()
    student = User.query.get(post_data.get('user')['uni'])
    classes_res = []
    for c in student.classes:
        c_res = {
            'ticker' :  '{}{}-{}'.format(c.course.dept_short, c.course.number, str(c.course.section).zfill(3)),
            'class' : str(c.course.title),
            'time' : str(c.course.day) + " " +  str(c.course.time),
            'professor' : c.course.faculty,
        }
        classes_res.append(c_res)
    response_object['seats'] = classes_res
    return jsonify(response_object)

'''
ORDER FUNCTIONS
'''
@app.route('/addOrder', methods=['POST'])
def add_order():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    course = Course.query.get(post_data.get('course'))
    student = User.query.get(post_data.get('user')['uni'])
    side=post_data.get('side')
    response_object['executed'] = 0

    if (side == 'SELL' and Seat.query.filter_by(student=student,course=course).first()) or side == 'BUY':
        order = Order(course=course, student=student, price=post_data.get('price'), side=side)
        db.session.add(order)
        db.session.commit()
        response_object['message'] = 'Order created'

        response_object['executed'] = 1
    else:
        response_object['message'] = 'Invalid order: no position in course'

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

'''
USER FUNCTIONS
'''
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

@app.route('/users', methods=['GET'])
def all_users():
    from models import User
    users = ''
    for user in User.query.all():
        users += '<p>{}</p>'.format(user.uni)
    return '%s' % users

'''
ACTIONS
'''
@app.route('/execute', methods=['PUT'])
def execute():
    response_object = {'status': 'success'}
    response_object['message'] = 'Invalid order: '
    response_object['executed'] = 0
    put_data = request.get_json()
    o = Order.query.get(put_data.get('order'))
    user = User.query.get(put_data.get('user')['uni'])

    seller = o.student # order placer
    buyer = user # you're executing their sell order
    if o.side == 'BUY':
        seller = user #you're executing their buy order
        buyer = o.student # order placer

    seat = Seat.query.filter_by(student=seller,course=o.course).first()
    if seat:
        if buyer.credits >= o.price:
            if seller != buyer:
                buyer.credits -= o.price
                seller.credits += o.price
                seat.student = buyer

                Order.query.filter_by(id=put_data.get('order')).delete()
                db.session.add(buyer)
                db.session.add(seller)
                db.session.add(seat)
                db.session.commit()
                response_object['message'] = 'Order executed'
                response_object['executed'] = 1
            else:
                response_object['message'] += ' buyer cannot be seller!'
        else:
            response_object['message'] += ' {} does not have enough credits ({}) for price ({})'.format(buyer, buyer.credits, o.price)
    else:
        response_object['message'] += ' seat in {} by {} not found'.format(o.course, seller)
    return jsonify(response_object)

@app.route('/delete', methods=['PUT'])
def delete():
    response_object = {'status': 'success'}
    response_object['message'] = 'Order could not be deleted '
    put_data = request.get_json()
    o = Order.query.get(put_data.get('order'))
    user = User.query.get(put_data.get('user')['uni'])
    response_object['executed'] = 0


    if o.student == user:
        Order.query.filter_by(id=put_data.get('order')).delete()
        db.session.commit()
        response_object['message'] = 'Order deleted'
        response_object['executed'] = 1
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

'''
ADMIN VIEW
'''
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



if __name__ == '__main__':
    app.run()
