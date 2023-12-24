from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        
        new_booking = Booking(name=name, email=email, phone=phone, date=date)
        db.session.add(new_booking)
        db.session.commit()
        
        return redirect(url_for('booking'))
    else:
        bookings = Booking.query.all()
        return render_template('booking.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)
