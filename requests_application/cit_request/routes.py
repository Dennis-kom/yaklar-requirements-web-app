from flask import Blueprint, render_template, request, redirect, url_for
from requests_application.app import db
from requests_application.cit_request.models import CitRequest
from datetime import datetime

cit_request = Blueprint('cit_request', __name__, template_folder='templates')

request_status = {0: 'התקבל', 1: 'הועבר לאישור', 2: 'אושר', 3: 'נדחה' }

@cit_request.route('/view')
def view():
    requests = CitRequest.query.all()
    return render_template('cit_request/viewall.html', requests=requests)

@cit_request.route('/viewall')
def viewall():
    requests = CitRequest.query.all()
    return render_template('cit_requests/viewall.html', requests=requests)

@cit_request.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        requester_name = request.form['requester_name']
        location = request.form['location']
        target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        request_content = request.form['content']
        people_amount = int(request.form['people_amount'])
        status = request_status[0]

        new_request = CitRequest(
            requester_name=requester_name,
            target_date=target_date,
            start_time=start_time,
            end_time=end_time,
            request_content=request_content,
            location=location,
            people_amount=people_amount,
            status=status
        )


        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('cit_request.viewall'))

    return render_template('cit_requests/create.html')

@cit_request.route('/update/<int:request_id>', methods=['GET', 'POST'])
def update(request_id):
    request_to_update = CitRequest.query.get_or_404(request_id)

    if request.method == 'POST':
        request_to_update.requester_name = request.form['requester_name']
        request_to_update.location = request.form['location']
        request_to_update.target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d').date()
        request_to_update.start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        request_to_update.end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        request_to_update.request_content = request.form['request_content']
        request_to_update.people_amount = int(request.form['people_amount'])
        request_to_update.status = request_status[int(request.form['status'])]

        db.session.commit()

        return redirect(url_for('cit_request.viewall'))

    return render_template('cit_request/update.html', cit_request=request_to_update)
