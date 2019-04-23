from flask import Flask, jsonify
from flask_cors import CORS

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


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/orders', methods=['GET'])
def all_orders():
    return jsonify({
        'status': 'success',
        'orders': ORDERS
    })

if __name__ == '__main__':
    app.run()
