from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key="asdsgdsadf324][pkj"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/pmt?charset=utf8mb4" % quote('@Phi100203')
#Abc111@
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True




db = SQLAlchemy(app=app)
login = LoginManager(app=app)