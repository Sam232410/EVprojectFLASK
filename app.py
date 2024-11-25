import csv
from flask import Flask, jsonify, render_template, request
import pandas as pd
import pickle
import numpy as np

from flask import Flask, render_template, request, redirect, url_for, flash, session # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_mysqldb import MySQL # type: ignore
from datetime import datetime
import re

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sam@localhost/evUSERS'  # Your MySQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # For flash messages and session

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)



# Path to the CSV file
CSV_FILE = 'data/data.csv'

def read_csv_file():
    """Reads the CSV file and returns the data."""
    with open(CSV_FILE, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data



# Load the trained model
model = pickle.load(open("model.pkl", "rb"))

# Load dataset to get vehicle-related data
data = pd.read_csv("data.csv")

# Extract unique vehicle names for the dropdown
vehicle_names = data['Make'].unique()






# @app.route('/')
# def index():
#     return render_template('index.html')

# Route for the homepage
@app.route('/')
def loginpg():
    return render_template('login.html')


# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')  # Date as a string
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        role = request.form.get('role')

        # Password matching validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format!', 'error')
            return redirect(url_for('register'))

        # Check if email or phone already exists
        existing_user = User.query.filter((User.email == email) | (User.phone == phone)).first()
        if existing_user:
            flash('Email or Phone number already registered. Please use a different one.', 'error')
            return redirect(url_for('register'))

        # Convert DOB string to datetime object
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format! Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user and add to the database
        new_user = User(name=name, email=email, phone=phone, dob=dob, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Set session variables for the newly registered user
        session['user_id'] = new_user.id
        session['user_name'] = new_user.name
        session['user_role'] = new_user.role

        flash('Registration successful! Please log in to continue.', 'success')

        # Redirect to login page after successful registration
        return redirect(url_for('login'))  # Now it redirects to login page

    return render_template('registration.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the email or phone number from the form
        email_or_phone = request.form.get('email_or_phone')  # Use get() to avoid KeyError
        password = request.form.get('password')

        # Check if the user exists using email or phone
        user = User.query.filter(
            (User.email == email_or_phone) | (User.phone == email_or_phone)
        ).first()

        if user and check_password_hash(user.password, password):
            # Store user details in session
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome {user.name}! Login successful.', 'success')
            
            # Redirect based on user role
            if user.role == 'Driver':
                return redirect(url_for('driver'))  # Redirect to driver page if the role is Driver
            else:
                return redirect(url_for('index'))  # Redirect to welcome page if the role is not Driver
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('login'))  # Stay on login page if login fails

    return render_template('login.html')  # Use a separate template for login if needed





# Route for the welcome page after login (for roles other than 'Driver')
@app.route('/index')
def index():
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'error')
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    
    # Render the welcome page with the user's name
    return render_template('index.html', user_name=session.get('user_name'))

# Route for the driver page after login (for the 'Driver' role)
@app.route('/driver', methods=['GET', 'POST'])
def driver():
    if request.method == 'POST':
        try:
            battery_percentage = float(request.form['battery'])
            model_id = int(request.form['model_id'])

            default_features_dict = {
                1: [7.4, 160, 425, 170, 330, 78, 4607, 1800, 1479, 2735, 2490, 496, 405, 0, 0, 1, 0, 0, 0, 1, 0],
                2: [5.7, 190, 470, 250, 430, 83, 4783, 1852, 1448, 2856, 2605, 555, 470, 0, 1, 0, 0, 0, 0, 0, 1],
                3: [7.4, 160, 425, 170, 330, 78, 4607, 1800, 1479, 2735, 2490, 496, 405, 0, 0, 1, 0, 0, 0, 1, 0],
                4: [3.3, 261, 460, 377, 660, 82, 4694, 1849, 1443, 2875, 2232, 388, 561, 1, 0, 0, 0, 0, 1, 0, 0],
                5: [7.4, 160, 425, 170, 330, 78, 4607, 1800, 1479, 2735, 2490, 496, 405, 0, 0, 1, 0, 0, 0, 1, 0],
            }

            # Validate model ID
            if model_id not in default_features_dict:
                return render_template('predictFORdriver.html', prediction_text="Invalid model ID.")

            # Create feature vector
            default_features = default_features_dict[model_id]
            final_features = [battery_percentage] + default_features
            final_features = np.array(final_features).reshape(1, -1)

            # Validate feature vector length
            assert len(final_features[0]) == 22, f"Feature vector size mismatch! Expected 22 but got {len(final_features[0])}"

            # Predict and return the result
            prediction = model.predict(final_features)
            output = round(prediction[0], 2)
            return render_template('predictFORdriver.html', prediction_text=f'Predicted Range: {output} km')

        except ValueError:
            return render_template('predictFORdriver.html', prediction_text="Invalid input. Please enter a valid number for battery percentage.")
        except AssertionError as e:
            return render_template('predictFORdriver.html', prediction_text=f"Error: {str(e)}")
    else:
        return render_template('predictFORdriver.html', prediction_text="")









@app.route('/distribution')
def distribution():
    return render_template('distribution.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/pie')
def pie():
    return render_template('pie.html')

@app.route('/relation')
def relation():
    return render_template('relation.html')

@app.route('/dataset')
def dataset():
    # Read data from CSV file
    data = []
    with open('data/data.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # Read the header row
        for row in csvreader:
            data.append(row)
    return render_template('dataset.html', header=header, data=data)


@app.route('/data', methods=['GET'])
def get_data():
    action = request.args.get('action', 'headers')

    # Read CSV data
    data = read_csv_file()

    if action == 'headers':
        headers = data[0]  # First row is headers
        return jsonify(headers)
    
    elif action == 'column':
        selected_column = request.args.get('column')
        headers = data[0]

        # Check if the column exists
        if selected_column not in headers:
            return jsonify({'error': 'Invalid column', 'headers': headers}), 400
        
        column_index = headers.index(selected_column)
        column_data = [row[column_index] for row in data[1:]]  # Exclude header row

        return jsonify(column_data)
    
    elif action == 'pieData':
        selected_column = request.args.get('column')
        headers = data[0]

        if selected_column not in headers:
            return jsonify({'error': 'Invalid column', 'headers': headers}), 400
        
        column_index = headers.index(selected_column)
        column_data = [row[column_index] for row in data[1:]]
        
        # Count occurrences for pie chart
        value_counts = {}
        for value in column_data:
            value_counts[value] = value_counts.get(value, 0) + 1
        
        return jsonify(value_counts)
    

        
    elif action == 'conditionalCounts':
        selected_column = request.args.get('column')
        headers = data[0]

        # Ensure columns exist
        try:
            status_index = headers.index('Vehicle Status')
            selected_index = headers.index(selected_column)
        except ValueError:
            return jsonify({'error': 'Invalid column'}), 400
        
        counts = {}

        for row in data[1:]:
            status = row[status_index]
            value = row[selected_index]

            # Skip invalid rows
            if status not in ['0', '1'] or not value:
                continue
            
            if value not in counts:
                counts[value] = {'0': 0, '1': 0}
            
            counts[value][status] += 1

        return jsonify(counts)
    
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            battery_percentage = float(request.form['battery'])
            model_id = int(request.form['model_id'])

            default_features_dict = {
                1: [7.4, 160, 425, 170, 330, 78, 4607, 1800, 1479, 2735, 2490, 496, 405, 0, 0, 1, 0, 0, 0, 1, 0],
                2: [5.7, 190, 470, 250, 430, 83, 4783, 1852, 1448, 2856, 2605, 555, 470, 0, 1, 0, 0, 0, 0, 0, 1],
                3: [7.4, 160, 425, 170, 330, 78, 4607, 1800, 1479, 2735, 2490, 496, 405, 0, 0, 1, 0, 0, 0, 1, 0],
                4: [3.3, 261, 460, 377, 660, 82, 4694, 1849, 1443, 2875, 2232, 388, 561, 1, 0, 0, 0, 0, 1, 0, 0],
                5: [7.4, 160, 425, 170, 330, 78, 4607, 1800, 1479, 2735, 2490, 496, 405, 0, 0, 1, 0, 0, 0, 1, 0],
            }

            # Validate model ID
            if model_id not in default_features_dict:
                return render_template('predict.html', prediction_text="Invalid model ID.")

            # Create feature vector
            default_features = default_features_dict[model_id]
            final_features = [battery_percentage] + default_features
            final_features = np.array(final_features).reshape(1, -1)

            # Validate feature vector length
            assert len(final_features[0]) == 22, f"Feature vector size mismatch! Expected 22 but got {len(final_features[0])}"

            # Predict and return the result
            prediction = model.predict(final_features)
            output = round(prediction[0], 2)
            return render_template('predict.html', prediction_text=f'Predicted Range: {output} km')

        except ValueError:
            return render_template('predict.html', prediction_text="Invalid input. Please enter a valid number for battery percentage.")
        except AssertionError as e:
            return render_template('predict.html', prediction_text=f"Error: {str(e)}")
    else:
        return render_template('predict.html', prediction_text="")






if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables if they do not exist
    app.run(debug=True)







