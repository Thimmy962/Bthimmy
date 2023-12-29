from flask import Flask, render_template, request
from flask_migrate import Migrate
from datetime import datetime
import secrets
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

current_year = datetime.now().year

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://thimmy:Uydnv1$1@localhost/thimmy_car?charset=utf8mb4'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.context_processor
def custom_context():
    # Add custom data to the context
    return {
        'company': 'Thimmy',
        'year': current_year,
    }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def create_user(username, email, password):
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    print(new_user.password_hash)
    print("Done")
    db.session.add(new_user)
    db.session.commit()

if __name__ == "__main__":
    # You can call the create_user function with the desired parameters
    username = input('Username: ')
    mail = input('Mail: ')
    password = input('Password: ')
    
    create_user(username, mail, password)
