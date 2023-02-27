from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session
import model ,shcema
from db import engine , SessionLocal



#model.Base.metadata.create_all(bind=engine)
app = FastAPI()

'''@app.get('/home/{name}/{age}') # Past Parameter
def home(name:str , age:int):
    return {"detail":f" {name} is {age} years old"}'''

@app.get('/') # Past Parameter
def home():
    return {"detail":"Mohsen"}

def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/createuser' , response_model=shcema.User)
def createuseer(user:shcema.UserCreate , db:Session = Depends(getdb)):
    dbuser = db.query(model.User).filter(model.User.email == user.email).first()
    if dbuser:
        raise  HTTPException(status_code=400 , detail="Email Exist")
    newuser = model.User(email = user.email , Username =user.username , Pass = user.password)
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser


