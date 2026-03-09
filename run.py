from requests_application.app import create_app
from flask import session


app = create_app()

@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True  # refresh expiry on activity

def cleanup_on_exit():
    """Cleanup function to clear sessions when app exits"""
    with app.app_context():
        session.clear()



if __name__ == '__main__':
    with app.app_context():
        # Initialize database if needed
        from requests_application.app import db
        db.create_all()

    app.run(host='0.0.0.0', debug=True, threaded=True)




