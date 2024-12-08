from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_session import Session 
from flask_mail import Mail, Message
from src.config import Config

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf = CSRFProtect(app)
    mail.init_app(app)
    # Session(app)

    

    from src.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from src.routes.auth import main_bp
    app.register_blueprint(main_bp)

    from src.routes.store import store_bp
    app.register_blueprint(store_bp, url_prefix='/store-admin')
    
    from src.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/')
    @app.route('/home')
    def index():
        # Render the landing page directly
        return render_template('landing-page.html')

    return app
