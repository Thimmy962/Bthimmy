from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from datetime import datetime
import secrets
from models import db, User, Car

current_year = datetime.now().year

app = Flask(__name__)

# Configurations

username = "thimmy"
password = "Uydnv1$1"
host = "localhost"
db_name = "thimmy_car"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{db_name}?charset=utf8mb4'

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)




login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



# Functions

@app.context_processor
def custom_context():
    return {
        'company': 'Bthimmy',
        'year': current_year,
    }



@app.route("/")
def home():
    cars = Car.query.limit(10).all()
    print(cars)
    return render_template('homepage.html', cars=cars)


@app.route("/list")
def list():
    page = request.args.get('page', 1, type=int)
    cars = Car.query.paginate(page=page, per_page= 2)
    return render_template('list.html', cars = cars)



@app.route('/details/<car_id>')
def details(car_id):
    try:
        car = Car.query.filter_by(id=car_id).first()
        if not car:
            raise NoResultFound
    except NoResultFound:
        return redirect(url_for('home'))
    return render_template("detail.html", car=car)



@app.route('/edit/<car_id>', methods = ['POST', 'GET'])
@login_required
def edit(car_id):
    try:
            car = Car.query.filter_by(id=car_id).first()
            if not car:
                raise NoResultFound
                return redirect(url_for('admin'))
    except NoResultFound:
            return redirect(url_for('admin'))

    if request.method == 'GET':
        return render_template('edit.html', car = car)
    else:
        name = request.form['name']
        color = request.form['color']
        make = request.form['make']
        year = request.form['year']
        price = request.form['price']

        car.name = name
        car.color = color
        car.make = make
        car.year = year
        car.price = price

        db.session.commit()

        return redirect(url_for('details', car_id = car_id))
        


@app.route('/newcar', methods = ['POST', 'GET'])
@login_required
def newcar():
    if request.method == 'GET':
        return render_template('new-car.html')
    else:
        name = request.form['name']
        color = request.form['color']
        make = request.form['make']
        year = request.form['year']
        price = request.form['price']
        
        new_car = Car(name = name.title(), color = color.title(), make = make.title(), year = year, price = price)
        db.session.add(new_car)
        db.session.commit()
        return render_template(url_for('admin'))



@app.route('/delete/<car_id>')
@login_required
def delete(car_id):
        try:
            car = Car.query.filter_by(id=car_id).first()
            if not car:
                raise NoResultFound
        except NoResultFound:
            return redirect(url_for('home'))
        
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for("admin"))




@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username.title()).first()

        if user is None:
            return render_template('login.html', message='User Does Not Exist')

        elif not user.check_password(password):
            return render_template('login.html', message='Password Does  not Match')

        else:
            login_user(user)
            # next = request.args.get('next')
            return redirect(url_for('admin'))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))




@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username'].title()
        password = request.form['password']
        mail = request.form['mail'].lower()
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        existing_user = User.query.filter_by(username = username).first()
        existing_mail = User.query.filter_by(email = mail).first()

        if password != confirm_password:
            return render_template('register.html', message = 'Password Does Not Match')
        
        if existing_user:
            return render_template('register.html', message = 'Username already in use')
        
        elif existing_mail:
            return render_template('register.html', message = 'Mail Already in use')
        
        new_user = User(username=username, email=mail)
        new_user.set_password(password)
        print(len(new_user.password_hash))
        print("Done")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('admin'))
        





@app.route("/admin")
@login_required
def admin():
    
    page = request.args.get('page', 1, type=int)

    cars = Car.query.paginate(page=page, per_page= 2)

    return render_template('admin.html', cars = cars)


if __name__ == '__main__':
    app.run(debug=True)
