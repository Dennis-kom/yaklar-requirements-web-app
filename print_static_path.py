from requests_application.app import create_app
import os

app = create_app()
print('Static folder:', app.static_folder)
print('Current working directory:', os.getcwd())
