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

class Publisher(abc.ABC):

    @abc.abstractmethod
    def subbiker(self):
        pass

    @abc.abstractmethod
    def subdriver(self):
        pass                                #ABC METHOD

    @abc.abstractmethod
    def notifybiker(self):
        pass

    @abc.abstractmethod
    def notifydriver(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------
class ConcretePublisher(Publisher):
    _observersbiker = []
    _observersdriver = []
    _state = None

    def subbiker(self):

        bikers = session.query(BIKERS).all()
        bikers_dict_list = [biker.__dict__ for biker in bikers]

        for biker in bikers_dict_list:
            biker.pop('_sa_instance_state', None)

        bikers_json = json.dumps(bikers_dict_list)

        self._observersbiker = bikers_json
        print(self._observersbiker)

    def subdriver(self):

        bikers = session.query(CARS).all()
        bikers_dict_list = [biker.__dict__ for biker in bikers]

        for biker in bikers_dict_list:
            biker.pop('_sa_instance_state', None)

        bikers_json = json.dumps(bikers_dict_list)

        self._observersdriver = bikers_json
        print(self._observersdriver)

# ----------------------------------------------------------------------------------------------------------------------
    def notifybiker(self):
        with app.app_context():
            print('Notifying observers...')
            observers_list = json.loads(self._observersbiker)
            names = [biker_dict['mo_Name_BIKER'] for biker_dict in observers_list]
            print(names)
            matching_bikers = BIKERS.query.filter(BIKERS.mo_Name_BIKER.in_(names)).all()
            for biker in matching_bikers:
                print(f'{biker.mo_Name_BIKER} can ride {biker.mo_Can_distance_BIKER} miles')


    def notifydriver(self):
        with app.app_context():
            print('Notifying observers...')
            observers_list = json.loads(self._observersdriver)
            names = [biker_dict['mo_Name_DRIVER'] for biker_dict in observers_list]
            print(names)
            matching_bikers = CARS.query.filter(CARS.mo_Name_DRIVER.in_(names)).all()
            for biker in matching_bikers:
                print(f'{biker.mo_Name_DRIVER} can ride {biker.mo_Can_distance_DRIVER} miles')



def operationmain(distance_order_int):
    i1 = ConcretePublisher()
    if distance_order_int >= 25:
        i1.subdriver()
        i1.notifydriver()
    else:
        i1.subbiker()
        i1.notifybiker()

@app.route('/order_process', methods=['GET', 'Post'])
def order_recive():
        if request.is_json:
            data = request.get_json()
            time.sleep(1)
            yes = "yes"
            orders = DBORDER(mo_order=data["j_order"], mo_distance=data["j_distance"], mo_State_order=yes)
            db.session.add(orders)
            db.session.commit()
            distance_order_int = int(data["j_distance"])
            print(distance_order_int)
            print("ORDER IS ACCEPT")
            print("Operation Observer Started")
            operationmain(distance_order_int)
            return jsonify({"msg": "Successfully Order Process"}), 201,
        else:
            return jsonify({"msg": "UnSuccessfully Order Process"}), 404



@app.route('/notify', methods=['GET', 'Post'])
def notify():
    return "------------OK DONE---------------"
    #return jsonify({"msg": "------------OK DONE---------------"}), 201,



if __name__ == "__main__":
    app.run(debug=True , port=6000)