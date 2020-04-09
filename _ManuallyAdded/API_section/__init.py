from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)  # , resources={r'*/api/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/plants', methods=['GET'])
    def get_plants():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants': formatted_plants[start:end],
            'total_plants': len(formatted_plants)
        })

    @app.route('/plants/<int:plant_id>')
    def get_plant(plant_id):
        plant = Plant.query.get(plant_id)
        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'plant': plant.format()
            })

    @app.route('/')
    def hello():
        return jsonify({'message': 'HELLO WORLD!'})

    @app.route('/smiley')
    def smiley():
        return ':)'

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    return app
