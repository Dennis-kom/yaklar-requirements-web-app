from flask import render_template, request, Blueprint, redirect, url_for, session

core = Blueprint('core', __name__)

@core.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('view_requests') is not None:
            return redirect(url_for('cit_request.viewall'))
        if request.form.get('add_request') is not None:
            return redirect(url_for('cit_request.create'))
        if request.form.get('edit_tuple') is not None:
            if session.get('username') not in ['DEV', 'Oz', 'Dan']:
                return redirect(url_for('core.index'))
            return redirect(url_for('cit_request.update_choice'))
        if request.form.get('add_user') is not None:
            if session.get('username') not in ['DEV', 'Oz', 'Dan']:
                return redirect(url_for('core.index'))
            return redirect(url_for('users.add_user'))

    if request.method == 'GET' and session.get('username') is None:
        return redirect(url_for('users.login'))
    return render_template('core/index.html')
