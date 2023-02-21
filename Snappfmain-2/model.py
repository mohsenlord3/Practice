from db_exten import db


class DBORDER(db.Model):

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True )
    mo_order = db.Column(db.String(20), unique=False, nullable=False)
    mo_distance = db.Column(db.String(20), unique=False, nullable=False)
    mo_State_order = db.Column(db.String(20), unique=False, nullable=True)
    #mo_accname_driver_order = db.Column(db.String(20), unique=False, nullable=False)


class BIKERS(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    mo_Name_BIKER = db.Column(db.String(20), unique=False, nullable=False)
    mo_Can_distance_BIKER= db.Column(db.String(20), unique=False, nullable=False)


class CARS(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    mo_Name_DRIVER = db.Column(db.String(20), unique=False, nullable=False)
    mo_Can_distance_DRIVER = db.Column(db.String(20), unique=False, nullable=False)