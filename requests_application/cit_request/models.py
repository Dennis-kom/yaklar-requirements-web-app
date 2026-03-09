from requests_application.app import db


class CitRequest(db.Model):
    __tablename__ = 'cit_request'

    id = db.Column(db.Integer, primary_key=True)
    requester_name = db.Column(db.String(100), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    request_content = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    people_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False) # make from dictionary

    def __repr__(self):
        return f'<CitRequest {self.name}>'