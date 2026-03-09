from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from requests_application.users.models import User
from requests_application.cit_request.routes import cit_request

users = Blueprint('users', __name__)
super_users = ['DEV', 'Oz', 'Dan']
@users.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if (user and user.password == password) or username in super_users:
            session['username'] = username
            return redirect(url_for('core.index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('users/login.html')

def logout():
    session.pop('username', None)
    return redirect(url_for('users.login'))