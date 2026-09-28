from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv("env")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

@ app.route('/hello-world', methods=['GET'])
def principal():
    return "OLá mundo"

if __name__ == "__main__":
    app.run(debug=True, port = 5000)