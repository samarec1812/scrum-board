from flask import Flask, jsonify, make_response
from apps import create_app

from config import DevelopmentConfig

app = create_app(DevelopmentConfig)


# @app.route('/index', methods=['GET'])
# def index():
#     return make_response(jsonify({'message': 'response'}), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
