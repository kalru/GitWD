# cur.execute('''CREATE TABLE meas (
#     time_recieved TIMESTAMP NOT NULL,
# 	time_device TIMESTAMP NOT NULL,
# 	device_id TEXT NOT NULL,
#  	temperature DOUBLE PRECISION NULL,
#   	bat_voltage DOUBLE PRECISION NULL
# );''')

from flask import Flask, request
from flask_restful import Resource, Api
import psycopg2

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        app.logger.info(request.get_json())
        app.logger.info(request.form)
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

        con = psycopg2.connect(database="johndb", user="john",
                               password="john", host="35.204.209.194", port="5432")
        app.logger.info('Database opened successfully')
        cur = con.cursor()

        cur.execute("INSERT INTO meas (time_recieved,time_device,device_id,temperature,bat_voltage)  VALUES (%s,%s,%s,%s,%s)",
                    (request.get_json()['metadata']['time'], psycopg2.TimestampFromTicks(int(request.get_json()['payload_fields']['time'])), request.get_json()['dev_id'], float(request.get_json()['payload_fields']['pcbtemp']), float(request.get_json()['payload_fields']['vbat']),))

        con.commit()
        app.logger.info("Operation done successfully")
        con.close()
        return {'hellsso': 'post', 's1': s1, 's2': s2}


api.add_resource(HelloWorld, '/', '/<string:s1>', '/<string:s1>/<string:s2>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
