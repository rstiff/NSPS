from flask import Flask, render_template, request, url_for, flash, session, redirect
import mysql.connector


app = Flask(__name__)

# secret key
app.secret_key = 'thisismysecretkey'

# database connection
con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='thsrocks',
    database='NSPS'
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = con.cursor(dictionary=True)
        query = 'SELECT * FROM users WHERE username = %s AND password = %s'
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        # authenticate username/password
        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.")
    
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = con.cursor()
        query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        cursor.execute(query, (username, password))
        con.commit()

        flash("User registered successfully!")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    

@app.route('/about')
def about_us():
    return render_template("about.html")

@app.route('/contact')
def contact_us():
    return render_template('contact.html')

@app.route('/laction')
def Located():
    return render_template('laction.html')


@app.route('/signupforclass', methods=['GET', 'POST'])
def signupForClass():
    success_message = None
    if request.method == 'POST':
        # Process form data
        full_name = request.form['fullName']
        email = request.form['email']
        class_category = request.form['classCategory']
        preferred_date = request.form['preferredDate']
        trainer = request.form['trainer']

        # Here you would typically save the data to the database

        success_message = "Successfully signed up for class!"
        flash(success_message)  # Store the success message in the flash context

    return render_template('signupforclass.html', success_message=success_message)

@app.route('/packages')
def packeges():

    return render_template('packages.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
