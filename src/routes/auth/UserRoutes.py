"""

Authentication Blueprint Module
-----------------------------

This module handles all authentication-related routes and functionality using Google OAuth2.0.
Users must have @g.msuiit.edu.ph email addresses.

Key Components:
    - Google OAuth2.0 integration
    - Session management
    - Protected route handling
    - Login/logout functionality

Routes:
    - /login: Displays login page
    - /dashboard: Protected route for authenticated users
    - /google/callback: Handles OAuth2.0 response
    - /logout: Handles user session termination


"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, current_app, make_response, g
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests
import json
from src.models import User, Session
from src.utils import init_session
from src.models import Item, Store, Admin



auth_bp = Blueprint('auth', __name__)

main_bp = Blueprint('main', __name__)

# Middleware to intercept protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return redirect(url_for('auth.login'))
            
        session_data = Session.get_session(session_id)
        if not session_data:
            return redirect(url_for('auth.login'))
            
        g.user = json.loads(session_data['user_data'])
        return f(*args, **kwargs)
    return decorated_function

# Route where the user goes when they login
@auth_bp.route('/login')
def login():
    return render_template('auth/userLogin.html')

# The dashboard of LunchKit
# The protected part of the application

# AI's ISSUE STARTS HERE. #
    #======= DISPLAYING THE ITEMS =====#
@main_bp.route('/home')
@login_required
def dashboard():
    items = Item.get_items()
    session_id = request.cookies.get('session_id')
    if session_id:
        session = Session.get_session(session_id)
        if session:
            # Parse the JSON string from user_data
            user_data = json.loads(session['user_data'])
    return render_template('user/dashboard.html', user=g.user, items = items, user_data=user_data)



    #====== DISPLAY SHOPS INTO A LOGGED-IN CUSTOMER =====#
@main_bp.route('/stores')
@login_required
def store_list_page():
    stores = Store.get_stores()
    return render_template('user/storeList.html', user=g.user, stores = stores)


# The endpoint that handles user creation after google authentication
@auth_bp.route('/google/callback', methods=['POST'])
def google_callback():
    try:
        # Get the token from the request
        data = request.get_json()
        
        if not data or 'credential' not in data:
            print("No credential found in request")  # Debug print
            return {'error': 'No credential provided'}, 400

        token = data['credential']

        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            current_app.config['GOOGLE_CLIENT_ID'],
            clock_skew_in_seconds=60  # Add some tolerance for clock skew
        )

       

        # Get user info from the verified token
        user_data = {
            'google_id': idinfo.get('sub'),
            'name': idinfo.get('name'),
            'email': idinfo.get('email'),
            # 'picture': idinfo.get('picture')
        }
        
        # Verify email domain
        if not user_data['email'].endswith('@g.msuiit.edu.ph'):
            return {'error': 'Invalid email domain'}, 403
        

        try:
            # Get that user in the db
            user = User.get_user_by_google_id(user_data['google_id'])
            
            if user:
                # If user exists then update, maybe relative information has changed
                fresh_user = User.update_user(user_data['name'], user_data['google_id'])
            else:
                # If not then create a new user
                fresh_user = User.create_user(user_data['google_id'],user_data['name'], user_data['email'])
            
            if(fresh_user):
                # Get the user data from the filtered user after db calls
                admin = Admin.get_admin(fresh_user['email'])
                if admin:
                    isAdmin = True
                else:
                    isAdmin = False

                user_data = {
                    'google_id': fresh_user['google_id'],
                    'email': fresh_user['email'],
                    'name': fresh_user['username'],
                    'isAdmin': isAdmin
                }

                # Initialize the session
                session_id = init_session(user_data)

                message = f"Welcome to Lunchkit {user_data['name']}"

                # Generate the response, if all goes well then user gets redirected to the protected route 
                response = make_response({'success': True, 'message': message ,'redirect': url_for('main.dashboard')})               

                # Create the cookie to be used for verification
                response.set_cookie(
                'session_id', 
                session_id,
                httponly=True,
                secure=current_app.config['SESSION_COOKIE_SECURE'],
                max_age=int(current_app.config['PERMANENT_SESSION_LIFETIME'].total_seconds())
                )
            
            return response
            
        except Exception as e:
            print(f"Database error: {str(e)}")
            return 'Database error occurred', 500
        

    except ValueError as e:
        print(f"Token verification failed: {str(e)}")  # Debug print
        return {'error': f'Token verification failed: {str(e)}'}, 401
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug print
        return {'error': 'An unexpected error occurred'}, 500


# Logout handler
@auth_bp.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        Session.delete_session(session_id)
    
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('session_id')
    return response