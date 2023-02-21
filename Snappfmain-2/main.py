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
@app.route('/menu' , methods = ['Post'])
def menurote():
    if request.is_json:
        data = request.get_json()
        j_menu = data.get('j_menu')
        menu = {
            "joje" : "25000" ,
            "Morgh": "355000"
        }

        return jsonify({"msg": "Successfully ORDER" ,"Menu":menu}), 201
    else:
        return jsonify({"msg": "Invalid request"}), 400

                                      #-----Menu_Route-----
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/order_receive' , methods = ['Post'])
def reg():
    if request.is_json:

        data = request.get_json()
        j_order = data.get('j_order')
        j_distance = data.get('j_distance')
        headers = {'Content-Type': 'application/json'}
        res = requests.post('http://127.0.0.1:5001/order_process', json=data, headers=headers)
        return jsonify({"msg": "Successfully ORDER"}), 201
    else:
        return jsonify({"msg": "Invalid request"}), 400

#-----------------------------------------------------------------------------------------------------------------------

@app.route('/registerdriver' , methods = ['Post'])
def registerdriver():
    if request.is_json:
        data = request.get_json()
        j_Name_DRIVER = data.get('j_Name_DRIVER')
        j_Can_distance_DRIVER = data.get('j_Can_distance_DRIVER')
        new_driver = CARS(mo_Name_DRIVER=j_Name_DRIVER , mo_Can_distance_DRIVER=j_Can_distance_DRIVER)
        db.session.add(new_driver)
        db.session.commit()
        return jsonify({"msg": "Successfully Register Driver"}), 201
    else:
        return jsonify({"msg": "UnSuccessfully Register Driver"}), 400


@app.route('/registerbikers' , methods = ['Post'])
def registerbikers():
    if request.is_json:
        data = request.get_json()
        j_Name_Biker = data.get('j_Name_Biker')
        j_Can_distance_Biker = data.get('j_Can_distance_Biker')
        new_biker = BIKERS(mo_Name_BIKER=j_Name_Biker , mo_Can_distance_BIKER=j_Can_distance_Biker)
        db.session.add(new_biker)
        db.session.commit()
        return jsonify({"msg": "Successfully Register Biker"}), 201
    else:
        return jsonify({"msg": "UnSuccessfully Register Biker"}), 400

#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)



