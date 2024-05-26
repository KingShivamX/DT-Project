from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Request, db
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        prn = request.form['prn']
        password = request.form['password']
        user = User.query.filter_by(prn=prn).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('request_access'))
        else:
            flash('Invalid PRN or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        prn = request.form['prn']
        password = request.form['password']
        existing_user = User.query.filter_by(prn=prn).first()
        if existing_user:
            flash('PRN already registered. Please log in.', 'error')
        else:
            new_user = User(username=username, prn=prn)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/request_access', methods=['GET', 'POST'])
@login_required
def request_access():
    if request.method == 'POST':
        name = request.form['name']
        prn = request.form['prn']
        reason = request.form['reason']
        new_request = Request(user_id=current_user.id, name=name, prn=prn, reason=reason)
        db.session.add(new_request)
        db.session.commit()
        flash('Request sent successfully.', 'success')
        return redirect(url_for('previous_requests'))
    return render_template('request_access.html')

@app.route('/previous_requests')
@login_required
def previous_requests():
    requests = Request.query.filter_by(user_id=current_user.id).all()
    return render_template('previous_requests.html', requests=requests)
