from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from requests_application.app import db
from requests_application.cit_request.models import CitRequest
from datetime import datetime, timedelta

cit_request = Blueprint('cit_request', __name__, template_folder='templates')

request_status = {0: 'התקבל', 1: 'הועבר לאישור', 2: 'אושר', 3: 'נדחה',4: 'אושר בכפוף ל'}

@cit_request.route('/delete/<int:request_id>', methods=['POST'])
def delete_request(request_id):
    request_to_delete = CitRequest.query.get_or_404(request_id)

    try:
        db.session.delete(request_to_delete)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Request deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'database_error'}), 500

def mandatory_content_approve(text: str):
    missing_parameters = []
    mandatory_components ={"תדריך": ['יקל"ר', 'יקלר'],"מיגון":['מיגון', 'ממ"ד', 'ממד','מקלט'] }
    for topic, words in mandatory_components.items():
        for word in words:
            if word in text:
                missing_parameters.append(topic)

    return missing_parameters

@cit_request.route('/view')
def view():
    requests = CitRequest.query.all()
    return render_template('cit_request/viewall.html', requests=requests)

@cit_request.route('/viewall')
def viewall():
    today = datetime.now().date()
    ten_days_later = today - timedelta(days=30)
    requests = CitRequest.query.filter(
        #CitRequest.target_date >= today,
        CitRequest.target_date >= ten_days_later
    ).all()
    return render_template('cit_requests/viewall.html', requests=requests)

@cit_request.route('/create', methods=['GET', 'POST'])
def create():


    if request.method == 'POST':
        requester_name = request.form['requester_name']
        location = request.form['location']
        target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        shelter = request.form.get('shelter')
        authority =request.form.get('authority')
        warning = request.form.get('warning')
        sequrity = request.form.get('sequrity')
        contact = request.form.get('contact')
        request_content = request.form['content']
        people_amount = int(request.form['people_amount'])
        status = request_status[0]
        full_content =  "תוכן:" + "\n" + request_content + "\n" + "מיגון:" + shelter + "\n" + "יקלר:" + authority + "\n" + "התרעה:" + warning + "\n" + "אבטחה:" + sequrity + "\n" + "איש קשר:" + contact

        new_request = CitRequest(
            requester_name=requester_name,
            target_date=target_date,
            start_time=start_time,
            end_time=end_time,
            request_content=full_content,
            location=location,
            people_amount=people_amount,
            status=status
        )


        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('cit_request.viewall'))

    return render_template('cit_requests/create.html')

@cit_request.route('/update', methods=['GET', 'POST'])
def update_choice():
    requests = CitRequest.query.all()
    if request.method == 'POST':
        selected_request_id = request.form['selected_id']
        return redirect(url_for('cit_request.update', request_id=selected_request_id))
    return render_template('cit_requests/update_choice.html', requests=requests)

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
        request_to_update.shelter = request.form['shelter']
        request_to_update.authority = request.form['authority']
        request_to_update.warning = request.form['warning']
        request_to_update.sequrity = request.form['sequrity']
        request_to_update.contact = request.form['contact']

        db.session.commit()

        return redirect(url_for('cit_request.viewall'))

    return render_template('cit_requests/update.html', cit_request=request_to_update)

@cit_request.route('/delete/<int:request_id>')
def delete(request_id):
    request_to_delete = CitRequest.query.get_or_404(request_id)
    db.session.delete(request_to_delete)
    db.session.commit()
    return redirect(url_for('cit_request.viewall'))