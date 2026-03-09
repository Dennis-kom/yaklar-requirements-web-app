from flask import render_template, request, Blueprint, redirect, url_for, session

core = Blueprint('core', __name__)

@core.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('view_requests') is not None:
            return redirect(url_for('cit_request.viewall'))
        if request.form.get('add_request') is not None:
            return redirect(url_for('cit_request.create'))

    if request.method == 'GET' and session.get('username') is None:
        return redirect(url_for('users.login'))
    return render_template('core/index.html')
