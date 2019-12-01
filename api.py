from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'get'}

    def put(self):
        return {'hello': 'put'}

    def post(self, s1='', s2=''):
        app.logger.info(request.form)
        return {'hellsso': 'post', 's1': s1, 's2': s2}


api.add_resource(HelloWorld, '/', '/<string:s1>', '/<string:s1>/<string:s2>')

if __name__ == '__main__':
    app.run(debug=True)
