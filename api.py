from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        app.logger.info(request.get_data())
        return {'hello': 'get'}

    def put(self):
        return {'hello': 'put'}

    def post(self, s1='', s2=''):
        app.logger.info(request.get_json()['app_id'])
        app.logger.info(request.get_json()['dev_id'])
        app.logger.info(request.get_json()['payload_fields']['pcbtemp'])
        app.logger.info(request.get_json()['payload_fields']['time'])
        app.logger.info(request.get_json()['payload_fields']['vbat'])
        app.logger.info(request.get_json()['metadata']['time'])
        # simulated doesn't have gateway
        if 'gateways' in request.get_json()['metadata']:
            for g in request.get_json()['metadata']['gateways']:
                app.logger.info(g['gtw_id'])
        else:
            app.logger.info('No gateway used... it was probably simulated')
        return {'hellsso': 'post', 's1': s1, 's2': s2}


api.add_resource(HelloWorld, '/', '/<string:s1>', '/<string:s1>/<string:s2>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
