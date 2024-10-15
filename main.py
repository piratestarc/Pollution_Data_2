from multiprocessing.resource_tracker import register
from dateutil.relativedelta import relativedelta
from datetime import datetime
from flask import Flask, render_template, flash, url_for
from flask_bootstrap import Bootstrap5
from werkzeug.utils import redirect

from form import MainForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Text, Column, ForeignKey, Boolean
from send_message import Email
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = "#python143"
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = '#prince143'
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# initialize the app with the extension
db.init_app(app)




# Define models
class User(db.Model):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True)
    vehicle_type = Column(String(250), unique=False, nullable=False)
    vehicle_number = Column(String(250), unique=True, nullable=False)
    vehicle_model = Column(String(250), nullable=True)
    register_owner = Column(String(250), nullable=False)
    current_owner = Column(String(250), nullable=False)
    phone_number = Column(Integer, nullable=False)

    # Establish a one-to-many relationship with BlogPost
    pollution = relationship('Pollution', back_populates='customer')
    insurance = relationship('Insurance', back_populates='customer')

class Pollution(db.Model):
    __tablename__ = "pollution"
    id = Column(Integer, primary_key=True)
    is_purchased = Column(String(250), unique=False, nullable=False)
    purchased_date = Column(String(250), nullable=False)
    expire_date = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('user_data.id'), nullable=False)


    # Define the back relationship to the User table
    customer = relationship('User', back_populates='pollution')




class Insurance(db.Model):
    __tablename__ = "insurance"
    id = Column(Integer, primary_key=True)
    is_purchased = Column(String(250), unique=False, nullable=False)
    customer_id = Column(Integer, ForeignKey('user_data.id'), nullable=False)
    policy_number = Column(String(250), nullable=False , unique=True)
    purchased_date = Column(String(250), nullable=False)
    expire_date = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    #establishing the relationship between user_data and insurance
    customer = relationship('User', back_populates='insurance')







with app.app_context():
    db.create_all()
@app.route("/",methods=["GET","POST"])
def hello_world():




    form = MainForm()


    if form.validate_on_submit():
        with app.app_context():
            is_register = db.session.execute(db.select(User).where(User.vehicle_number == form.vehicle_no.data)).scalar()
            print(is_register)
        if not is_register:
            print("Not in the dict")


            #User data Table
            vehicle_type = form.vehicle_Type.data
            vehicle_no = form.vehicle_no.data
            vehicle_model = form.vehicle_model.data
            register_owner = form.register_owner.data
            current_owner = form.current_owner.data
            phone_number = form.phone_number.data

            #creating a new data for the customer
            with app.app_context():
                new_user = User(vehicle_type=vehicle_type,
                                vehicle_number=vehicle_no,
                                vehicle_model=vehicle_model,
                                register_owner=register_owner,
                                current_owner=current_owner,
                                phone_number=phone_number)
                db.session.add(new_user)
                db.session.commit()


            #pollution table

            pollution = form.pollution.data
            if pollution == 'Yes':
                today = datetime.now().date()
                pollution_purchased_date = today
                pollution_expire_date = today + relativedelta(months=int(form.pollution_expire.data))
                pollution_expire = pollution_expire_date
                pollution_price = form.pollution_price.data
                with app.app_context():
                    customer = db.session.execute(db.select(User).where(User.vehicle_number == vehicle_no)).scalar()
                    new_user = Pollution(is_purchased=pollution,
                                    purchased_date=pollution_purchased_date,
                                    expire_date=pollution_expire,

                                    price=pollution_price,
                                    customer_id=customer.id)
                    db.session.add(new_user)
                    db.session.commit()

            # insurance table
            insurance = form.insurance.data
            if insurance == 'Yes':
                today = datetime.now().date()
                insurance_purchased_date = today
                insurance_expire_date = today + relativedelta(months=int(form.insurance_expire.data))
                insurance_expire = insurance_expire_date
                insurance_price = form.insurance_price.data
                policy_number = form.policy_number.data
                with app.app_context():
                    customer = db.session.execute(db.select(User).where(User.vehicle_number == vehicle_no)).scalar()
                    new_user = Insurance(is_purchased=insurance,
                                    purchased_date=insurance_purchased_date,
                                    expire_date=insurance_expire,
                                    policy_number=policy_number,
                                    price=insurance_price,
                                    customer_id=customer.id)
                    db.session.add(new_user)
                    db.session.commit()


            flash('New Data has been added', 'success')
            return redirect(url_for("hello_world"))
        else:
            flash("The Vehicle Number is already Registered","danger")
            return redirect(url_for("hello_world"))





    return render_template("index.html", form =form)

@app.route("/email")
def email():
    count = 0
    current_date = datetime.now().date()
    tommorow = str(current_date + relativedelta(days=1))
    with app.app_context():
        is_any_expiry_pollution = db.session.execute(db.select(Pollution).where(Pollution.expire_date == tommorow)).all()
        is_any_expiry_insaurance = db.session.execute(db.select(Insurance).where(Insurance.expire_date == tommorow)).all()

        if is_any_expiry_insaurance:
            print("Insaurance")
            Email(is_any_expiry_insaurance,"Insurance")
            count += 1


        if is_any_expiry_pollution:
            print("Pollution")
            is_any_expiry_pollution = db.session.execute(db.select(Pollution).where(Pollution.expire_date == tommorow)).scalars()
            Email(is_any_expiry_pollution,"Pollution")
            count += 1

        if not is_any_expiry_insaurance:
            if not is_any_expiry_pollution:
                return "No Vehicle Pollution or Insurance is Getting Expired"










if __name__ == "__main__":
    app.run(debug=True)
