from db import Base
from sqlalchemy import Column , Integer ,String , Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    Username = Column(String)
    Pass = Column(String)


    #items = relationship("Item", back_populates="owner")