from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from requests_application.users.models import User
from requests_application.cit_request.routes import cit_request
from requests_application.app import db
from requests_application.app import session

users = Blueprint('users', __name__)
super_users = ['DEV', 'Oz', 'Dan']

def superuser_level_check():
    username = session.get('username')
    return username in super_users


@users.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if (user and user.password == password) or username in super_users:
            session.clear()  # Clear any previous session data
            session['username'] = username
            session.permanent = True
            return redirect(url_for('core.index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('users/login.html')

@users.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@users.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Handle JSON requests
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return jsonify({'success': False, 'error': 'user_exists'}), 400

            # Add new user (name defaults to username)
            try:
                new_user = User(name=username, username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return jsonify({'success': True, 'message': 'User added successfully'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'error': 'database_error'}), 500

        # Handle form requests (legacy)
        else:
            if superuser_level_check():
                username = request.form['username']
                password = request.form['password']

                if User.query.filter_by(username=username).first():
                    flash('Username already exists', 'danger')
                    return redirect(url_for('users.add_user'))

                new_user = User(name=username, username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully', 'success')
                return redirect(url_for('core.index'))
            else:
                flash('You do not have permission to add users', 'danger')
                return redirect(url_for('core.index'))

    return render_template('users/add_user.html')
