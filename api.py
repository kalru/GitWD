from flask import Flask, request, has_request_context
from flask.logging import default_handler
from flask_restful import Resource, Api
import logging

app = Flask(__name__)
api = Api(app)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'get'}

    def put(self):
        return {'hello': 'put'}

    def post(self, s1='', s2=''):
        app.logger.info(request.form)
        return {'hellsso': 'post', 's1': s1, 's2': s2}


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)

default_handler.setFormatter(formatter)

api.add_resource(HelloWorld, '/', '/<string:s1>', '/<string:s1>/<string:s2>')

if __name__ == '__main__':
    app.run(debug=True)
