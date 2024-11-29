import csv
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
import pickle
import numpy as np
import pandas as pd
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import smtplib
import plotly.express as px
import plotly.io as pio
import os




# Initialize Flask app and database
app = Flask(__name__)


# import os
# from sqlalchemy import create_engine

# mysql_host = os.getenv("localhost")
# mysql_user = os.getenv("root")
# mysql_password = os.getenv("sam")
# mysql_db = os.getenv("evUSERS")

# engine = create_engine(f'mysql+mysqldb://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}')



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sam@localhost/evUSERS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'


# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'email23testing@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'owpp amrr cdbi soog'         # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'email23testing@gmail.com'

# Initialize Flask-Mail and SQLAlchemy
mail = Mail(app)
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
    reset_token = db.Column(db.String(256), nullable=True)
    
    def __repr__(self):
        return f'<User {self.name}>'



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





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieving form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        role = request.form.get('role')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Password strength rules
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            flash('Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character.', 'error')
            return redirect(url_for('register'))

        # Check email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format!', 'error')
            return redirect(url_for('register'))

        # Check if email or phone already exists
        existing_user = User.query.filter((User.email == email) | (User.phone == phone)).first()
        if existing_user:
            flash('Email or Phone number already registered.', 'error')
            return redirect(url_for('register'))

        # Validate date of birth format
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'error')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Create a new user
        new_user = User(name=name, email=email, phone=phone, dob=dob, password=hashed_password, role=role)
        
        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()

            # Send a welcome email
            send_welcome_email(email, name)
            
            # Store user details in the session
            session['user_id'] = new_user.id
            session['user_name'] = new_user.name
            session['user_role'] = new_user.role

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))  # Redirect to login page
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('registration.html')





# Route for the registration page
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         dob = request.form.get('dob')  # Date as a string
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirmPassword')
#         role = request.form.get('role')

#         # Password matching validation
#         if password != confirm_password:
#             flash('Passwords do not match!', 'error')
#             return redirect(url_for('register'))

#         # Validate email format
#         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             flash('Invalid email format!', 'error')
#             return redirect(url_for('register'))

#         # Check if email or phone already exists
#         existing_user = User.query.filter((User.email == email) | (User.phone == phone)).first()
#         if existing_user:
#             flash('Email or Phone number already registered. Please use a different one.', 'error')
#             return redirect(url_for('register'))

#         # Convert DOB string to datetime object
#         try:
#             dob = datetime.strptime(dob, '%Y-%m-%d').date()
#         except ValueError:
#             flash('Invalid date format! Please use YYYY-MM-DD.', 'error')
#             return redirect(url_for('register'))

#         # Hash the password
#         hashed_password = generate_password_hash(password)

#         # Create a new user and add to the database
#         new_user = User(name=name, email=email, phone=phone, dob=dob, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()

#         # Set session variables for the newly registered user
#         session['user_id'] = new_user.id
#         session['user_name'] = new_user.name
#         session['user_role'] = new_user.role

#         flash('Registration successful! Please log in to continue.', 'success')

#         # Redirect to login page after successful registration
#         return redirect(url_for('login'))  # Now it redirects to login page

#     return render_template('registration.html')

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


#####FORGOT-PASSWORD


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a temporary password reset token
            reset_token = generate_password_hash(f"{email}{datetime.now()}", method='pbkdf2:sha256')
            user.reset_token = reset_token
            db.session.commit()  # Save the token to the database

            # Send password reset email
            try:
                reset_link = f"http://localhost:5000/reset_password?token={reset_token}"
                msg = Message(
                    'Password Reset Request',
                    recipients=[email],
                    body=f"Hi {user.name},\n\nClick the link below to reset your password:\n"
                         f"{reset_link}\n\n"
                         f"If you did not request a password reset, please ignore this email.\n\nBest regards,\nEV System Team"
                )
                mail.send(msg)
                flash('Password reset link sent to your email.', 'success')
            except Exception as e:
                print(f"Error sending email: {e}")
                flash('Error sending email. Please try again later.', 'error')
        else:
            flash('Email not registered.', 'error')

        return redirect(url_for('login'))
    return render_template('forgot_password.html')



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_token = request.args.get('token')  
    if not reset_token:
        flash("Invalid password reset request.", "error")
        return redirect(url_for('forgot_password'))

    user = User.query.filter_by(reset_token=reset_token).first()
    if not user:
        flash("Invalid or expired token.", "error")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return render_template('reset_password.html', token=reset_token)

        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
        user.reset_token = None  # Clear the reset token after password change
        db.session.commit()  # Save changes to the database

        flash("Your password has been successfully updated!", "success")
        return redirect(url_for('login'))  # Redirect to login page after success

    return render_template('reset_password.html', token=reset_token)


def send_welcome_email(email, name):
    try:
        msg = Message('Welcome to EV System', recipients=[email])
        msg.body = f"Hi {name},\n\nThank you for registering with us!\n\nBest regards,\nEV System Team"
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")










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

# @app.route('/status')
# def status():
#     return render_template('status.html')

# Add Working Condition and Charging Status based on Vehicle Status
data['Working Condition'] = data['Vehicle Status'].apply(lambda x: '1' if x == 1 else '0')
data['Charging Status'] = data['Vehicle Status'].apply(lambda x: '1' if x == 1 else '0')

# Get unique vehicle names (or makes)
vehicle_names = data['Make'].unique()

@app.route("/status", methods=["GET", "POST"])
def status():
    status_type = request.form.get("status_type", "Charging Status")
    
    # Initialize an empty DataFrame to store the randomly selected entries
    random_entries = pd.DataFrame()

    # Loop through each unique vehicle name and fetch a random entry
    for vehicle in vehicle_names:
        vehicle_data = data[data['Make'] == vehicle]  # Filter data for the current vehicle
        random_row = vehicle_data.sample(n=1)  # Randomly pick one row for this vehicle
        random_entries = pd.concat([random_entries, random_row])

    if status_type == "Charging Status":
        # Count the occurrences of Charging Status from random entries
        status_count = random_entries['Charging Status'].value_counts().reset_index()
        status_count.columns = ['Charging Status', 'Count']
    else:  # Working Condition
        # Count the occurrences of Working Condition from random entries
        status_count = random_entries['Working Condition'].value_counts().reset_index()
        status_count.columns = ['Working Condition', 'Count']

    # Generate the Plotly graph
    fig = px.bar(status_count, 
                 x=status_count.columns[0],  # This will be Charging Status or Working Condition
                 y="Count", 
                 title=f"{status_type} Count (Random Entry per Vehicle)",
                 labels={status_count.columns[0]: status_type, "Count": "Vehicle Count"})
    # Update bar color to orange
    fig.update_traces(marker_color="#FF7F50")
    fig.update_layout(
        width=1000,  # Chart width
        height=500,  # Chart height
        margin=dict(t=30, l=20, r=20, b=20),  # Margins: top, left, right, bottom
        title="Vehicle Status",
        # yaxis_range=[0, 7],  # Set the Y-axis range from 0 to 7
        hovermode="closest"
    )

    # Convert the Plotly graph to HTML to embed it in the webpage
    graph_html = pio.to_html(fig, full_html=False)

    return render_template("status.html", graph_html=graph_html, status_type=status_type)



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
    

        
    # elif action == 'conditionalCounts':
    #     selected_column = request.args.get('column')
    #     headers = data[0]

    #     # Ensure columns exist
    #     try:
    #         status_index = headers.index('Vehicle Status')
    #         selected_index = headers.index(selected_column)
    #     except ValueError:
    #         return jsonify({'error': 'Invalid column'}), 400
        
    #     counts = {}

    #     for row in data[1:]:
    #         status = row[status_index]
    #         value = row[selected_index]

    #         # Skip invalid rows
    #         if status not in ['0', '1'] or not value:
    #             continue
            
    #         if value not in counts:
    #             counts[value] = {'0': 0, '1': 0}
            
    #         counts[value][status] += 1

    #     return jsonify(counts)
    
    
    
    
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



####maintenance
@app.route("/maintenance")
def maintenance():
     # Aggregate total maintenance cost by vehicle make
    maintenance_by_make = data.groupby("Make")["Maintenance Cost"].mean().reset_index()

    # Convert to dictionaries for JSON usage
    maintenance_by_make = maintenance_by_make.to_dict(orient="records")

    return render_template("maintenance.html",
                           maintenance_by_make=maintenance_by_make)

    # # Aggregate maintenance cost by month
    # #monthly_maintenance = data.groupby("Month")["Maintenance Cost"].sum().reset_index()

    # # Aggregate average maintenance cost by vehicle make
    # avg_maintenance_by_make = data.groupby("Make")["Maintenance Cost"].mean().reset_index()

    # # Convert to dictionaries for JSON usage
    # #monthly_maintenance = monthly_maintenance.to_dict(orient="records")
    # avg_maintenance_by_make = avg_maintenance_by_make.to_dict(orient="records")

    # return render_template("maintenance.html",
    #                        avg_maintenance_by_make=avg_maintenance_by_make)


##########sharing notifications for overspeeding
# Function to send email notifications
# Function to send email notifications

# Define a mapping of driver names to email addresses
driver_email_map = {
    "chandu": "masettychandana@gmail.com",
    "praneetha": "praneethachutla13@gmail.com",
    "sahithya": "sahithyamadala@gmail.com",
    "samiksha": "waghsamiksha05@gmail.com",

    # Add more driver names and their emails here
}

# Function to send email notifications
def send_notification(driver_name, email):
    sender_email = "email23testing@gmail.com"  # Replace with your email
    sender_password = "owpp amrr cdbi soog"  # Replace with your app password
    subject = "Overspeeding Alert"
    message = f"Dear {driver_name},\n\nYou have been observed driving at speeds exceeding 120 km/h. Please adhere to the speed limits for safety.\n\nRegards,\nFleet Management Team"

    # Email setup
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, f"Subject: {subject}\n\n{message}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    

@app.route("/behavior")
def behavior():
    # Filter overspeeding drivers
    overspeeding = data[data["Speed"] > 120]
    
    # Group by driver name and get the top speed for each driver
    top_speed = overspeeding.groupby("Driver")["Speed"].max().reset_index(name="Top Speed")

    # Map email addresses to drivers
    top_speed["Email"] = top_speed["Driver"].apply(lambda x: driver_email_map.get(x, "email23testing@gmail.com"))

    # Convert to dictionary for passing to the template
    top_speed = top_speed.to_dict(orient="records")

    return render_template("behavior.html", drivers=top_speed)


@app.route("/notify", methods=["POST"])
def notify():
    driver_name = request.form.get("driver_name")
    email = request.form.get("email")

    if send_notification(driver_name, email):
        return jsonify({"success": True, "message": "Notification sent successfully."})
    else:
        return jsonify({"success": False, "message": "Failed to send notification."})






if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables if they do not exist
    app.run(debug=True)







