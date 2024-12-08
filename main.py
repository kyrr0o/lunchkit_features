import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Set before importing app

from src import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)