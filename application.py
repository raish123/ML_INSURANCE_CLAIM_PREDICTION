#this file we used to create front end for user to takes input from user and return the predicted result 
#for which we used flask framework for it  


from flask import Flask, render_template, redirect, request, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import UserModel, load_user,db,login
import os
from src.pipelines.prediction_pipeline import CustomData,PredictPipeline
from src.exception import CustomException
from src.logger import logging
import os,sys

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure the Flask web application with database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/INSURANCE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'defaultsecret')

#now binding the flask application with sqlalchemy class object this built in method init_app()
db.init_app(app)

#now binding the flask application with loginmanger class object(which manage the session of users)
login.init_app(app)

#customize the login process
login.login_view = "login"


# Create all the tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password_hash')

        # Check if the email or username already exists
        existing_user = UserModel.query.filter_by(email=email).first()
        
        if existing_user:
            msg = f'{username} already exists. Please login.'
            return render_template('login.html', context=msg)
        
        # Create a new user and save to the database
        new_user = UserModel(email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        msg = f'Congrats {username}, your account has been created successfully. Now you can login.'
        return render_template('index.html', context=msg)
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('prediction'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password_enter_login')

        # Check if the email and password match
        user = UserModel.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            msg = 'Welcome to the Prediction Page'
            return render_template('predict.html', context=msg)

        return render_template('register.html', context='Credentials do not match. Please register.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')



@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    if request.method == 'POST':
        # Get the data from the form
        age = request.form.get('age')
        sex = request.form.get('sex')
        bmi = request.form.get('bmi')
        children = request.form.get('children')
        smoker = request.form.get('smoker')
        region = request.form.get('region')
        charges = request.form.get('charges')

        #creating an object of CustomData class of prepdict_pipeline module
        cd = CustomData(age=age,sex=sex,bmi=bmi,children=children,smoker=smoker,region=region,charges=charges)

        #now getting df object by using customdata object and calling object method get_data_df
        df = cd.get_data_df()
        logging.info('Prediction datapoint coming from webpage\n%s', df)
        #now passing this parameter to Predict method of predictpipeline class
        #and getting the result
        #creating object of predictpipeline class
        pred = PredictPipeline()

        #now getting prediction result using Prediction methofd of predictpipeline class
        pred_result = pred.Predict(df)

        return render_template('result.html', result=pred_result[0])


    return render_template('predict.html')






if __name__ == '__main__':
    app.run(host='0.0.0.0')
