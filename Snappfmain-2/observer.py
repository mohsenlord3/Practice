from flask import Flask , request , jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from db_exten import db
import os.path
from model import DBORDER , CARS , BIKERS
import time
import abc
from random import randrange
import json
import rabbitpy
import pika
import uuid
                                        #-----Requirements-----
#-----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR,"project4.db")
db.init_app(app)
with app.app_context():                 #-----Setting_App-----
    #db.init_app(app)
    db.create_all()
    db.session.commit()
    session = Session(bind=db.engine)
#-----------------------------------------------------------------------------------------------------------------------
import abc
class Subject(abc.ABC):
    @abc.abstractmethod
    def attach(self, observer):
        pass





    @abc.abstractmethod
    def detach(self, observer):
        pass
    @abc.abstractmethod
    def notify(self):
        pass
#-----------------------------------------------------------------------------------------------------------------------
class ConcreteSubject(Subject):
    _observers = []
    _state = None

    def attach(self, observer):
        self._observers.append(observer)
        print(self._observers)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)
            print(self._observers)

#-----------------------------------------------------------------------------------------------------------------------
class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self, subject):
        pass
#-----------------------------------------------------------------------------------------------------------------------
class ConcreteObserver(Observer):

    def runrabbitmq(self):


        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='my_queue')
        message = {'message': "--------------------SENDING-------------------------------"}
        message_bytes = json.dumps(message).encode('utf-8')
        channel.basic_publish(exchange='', routing_key='my_queue', body=message_bytes)
        print(message)
        connection.close()

    def sendingrequest(self):

        headers = {'Content-Type': 'application/json'}
        res = requests.post('http://127.0.0.1:6000/notify', headers=headers)

    def update(self, subject):
        print(f"ConcreteObserver received update from ConcreteSubject with state {subject._state}")

        parameters = {
            'url': 'amqp://guest:guest@localhost:5672/%2F',
        }

        '''parameters = {
            'hostname': 'rabbitmq-hostname',
            'port': 5672,
            'username': 'username',
            'password': 'password',
            'virtual_host': '/'
        }'''
        try:
            connection = rabbitpy.Connection(**parameters)
            print("Connection to RabbitMQ is alive!")
            ConcreteObserver.runrabbitmq(self)

        except Exception as e:
            print("Failed to connect to RabbitMQ:", e)
            ConcreteObserver.sendingrequest(self)

        finally:
            connection.close()


@app.route('/order_process', methods=['GET', 'Post'])
def order_recive():
        if request.is_json:
            data = request.get_json()
            time.sleep(1)
            yes = "yes"


            subject = ConcreteSubject()
            observer = ConcreteObserver()


            subject.attach(observer)
            subject._state = "new_state"
            subject.notify()


            orders = DBORDER(mo_order=data["j_order"], mo_distance=data["j_distance"], mo_State_order=yes)
            db.session.add(orders)
            db.session.commit()
            return jsonify({"msg": "Successfully Order Process"}), 201,
        else:
            return jsonify({"msg": "UnSuccessfully Order Process"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)

    '''subject.detach(observer)
    subject._state = "other_state"
    subject.notify()'''