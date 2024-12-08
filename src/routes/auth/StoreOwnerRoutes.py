"""
Store Owner Authentication Module
-------------------------------

This module handles all authentication and registration functionality for store owners,
including signup, login, and session management.

Key Components:
    - Store owner registration and signup workflow
    - Password-based authentication with bcrypt
    - Session management and cookie handling
    - Protected route handling via decorators
    - Application status tracking (Default/Processing/Completed)

Routes:
    - /storeOwnerSign-up (GET): Display registration form
    - /storeOwnerSign-up/create (POST): Handle new registrations
    - /storeOwnerSign-up/handle-choice (POST): Manage duplicate registration choices
    - /storeOwnerLogin (GET): Display login form
    - /storeOwnerLogin (POST): Handle authentication
    - /register-store (GET): Display store registration form

"""
from flask import render_template,jsonify,url_for,current_app,request,make_response,redirect, g
from functools import wraps
import json

from src.routes.auth import auth_bp
from src.forms.StoreOwner.SignUpForm import StoreOwnerSignUpForm
from src.forms.StoreOwner.LoginForm import StoreOwnerLoginForm
from src.models.StoreOwner import StoreOwner
from src.models.Session import Session
import bcrypt
from src.utils.session import init_session


@auth_bp.route('/storeOwnerSign-up',methods=['GET'])
def ownerSignup():
    form = StoreOwnerSignUpForm()
    return render_template('auth/storeOwnerSign-up.html',form=form)


@auth_bp.route('/storeOwnerSign-up/create', methods=['POST'])
def storeowner_signup_create():
    form = StoreOwnerSignUpForm()
    
    if not form.validate_on_submit():
        errors = {}
        for field, field_errors in form.errors.items():
            errors[field] = field_errors[0]
        return jsonify({'success': False, 'errors': errors}), 400

    try:

        store_owner = StoreOwner.search_storeOwner(form.email.data)

        # Check if store owner exits
        if store_owner:

            # Check status of store Owner
            if store_owner['Application_Status'] == 'Default':

                # Ask the store owner if they want to proceed with old data or create new
                return jsonify({
                    'success': True,
                    'final_check': False,
                    'message': 'Existing application found',
                }), 409


            # If User has completed Application then no need to create again       
            if store_owner['Application_Status'] == 'Completed':
                return jsonify({'success': False,
                                'message': 'Store Registration and Owner Application already completed',
                                'shouldRedirect':False}), 400
            
            # If User has pending Application stop them from making another one
            if store_owner['Application_Status'] == 'Processing':
                return jsonify({'success': 'Waiting',
                                'message': f"Store Registration still in admin review for store with owner: {store_owner['OwnerName']}",
                                'shouldRedirect':False}), 400
            
        else:        



            # If store owner not cretead yet then create new
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())

            StoreOwner.create_storeOwner(
                form.ownername.data,
                form.email.data,
                form.mobile.data,
                hashed_password,
                'Default'
            )


            # If success return this response
            return jsonify({'success': True,
                            'message': 'Registration successful',
                            'shouldRedirect':True})
    
    

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    





# Route to be used handle call from choices derived after 309 state choice
@auth_bp.route('/storeOwnerSign-up/handle-choice', methods=['POST'])
def handle_owner_choice():
    try:
        choice = request.form.get('choice')
      
        # Return the Directly without modifying anything if they want their 
        if choice == 'use_previous':
            return jsonify({'success': True, 'message': 'Previous Owner Registration Preserved','shouldRedirect':True})

        # Update existing storeOwner if choice is overWrite   
        else:
            hashed_password = bcrypt.hashpw(
                request.form.get('password').encode('utf-8'),
                bcrypt.gensalt()
            )
            StoreOwner.update_storeOwner(
                request.form.get('ownername'),
                request.form.get('email'),
                request.form.get('mobile'),
                hashed_password,
                'Default'
            )

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'shouldRedirect': True,
            'final_check': True
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400



# Route for store owner login
@auth_bp.route('/storeOwnerLogin',methods=['GET'])
def ownerLogin():
    form = StoreOwnerLoginForm()
    return render_template('auth/storeOwnerLogin.html',form=form)



# The endpoint that handles storeOwner login
@auth_bp.route('/storeOwnerLogin',methods=['POST'])
def storeowner_login():

    # Specify form 
    form = StoreOwnerLoginForm()

    # Check form with form validators
    if not form.validate_on_submit():
        errors = {}
        for field, field_errors in form.errors.items():
            errors[field] = field_errors[0]
        return jsonify({'success': False, 'errors': errors}), 400
    
    try:

        # Checks if the store owner already in db
        valid_owner = StoreOwner.search_storeOwner(form.email.data)

        # Reject if not exits
        if not valid_owner:
            return jsonify({'success': False, 'message': 'Account not Found'})
        

        # Reject if passwords do not match
        if not bcrypt.checkpw(form.password.data.encode('utf-8'), valid_owner['Password'].encode('utf-8')):
            return jsonify({'success': False, 'message': 'Invalid password'})

        # Reject if Application Status is Processing
        if valid_owner['Application_Status'] == 'Processing':
            # return jsonify({'success': False, 'message': 'Store Registration still in Progress'})
            message = f"Welcome to LunchKit {valid_owner['OwnerName']} Pending"
            return jsonify({'success':True, 'message':message, 'redirect': url_for('store-admin.storecontentsPending', StoreOwnerId = valid_owner['StoreOwnerId']) })  
        
        # Reject if Account does not have valid store
        if valid_owner['Application_Status'] == 'Default':
            return jsonify({'success': False, 'message': 'Store Owner does not have registered store'})
        
        # Get the full owner data
        owner_data = {
            'store_owner': True,
            'owner_id': valid_owner['StoreOwnerId'],
            'owner_name': valid_owner['OwnerName'],
            'application_status': valid_owner['Application_Status'],
            'email': valid_owner['Email'],
            'mobile': valid_owner['Mobile_Num']
        }

        # Use the owner data to make session
        session_id = init_session(owner_data)

        message = f"Welcome to LunchKit Stores {owner_data['owner_name']}"

        # Specify the response config
        response = jsonify({'success':True, 'message':message, 'redirect': url_for('store-admin.storecontents', StoreOwnerId = owner_data['owner_id']) })       

        # Initialize the cookie for response in the frontend
        response.set_cookie(
            'session_id',
            session_id,
            httponly=True,
            secure=current_app.config['SESSION_COOKIE_SECURE'],
            max_age=int(current_app.config['PERMANENT_SESSION_LIFETIME_OWNER'].total_seconds())
        )

        # Returns the response
        return response
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    

# Middleware handler for store owner routes
def login_required_owner(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return redirect(url_for('auth.ownerLogin'))
            
        session_data = Session.get_session(session_id)
        if not session_data:
            return redirect(url_for('auth.ownerLogin'))
            
        user_data = json.loads(session_data['user_data'])

        if not user_data.get('store_owner'):
            return redirect(url_for('auth.ownerLogin'))

        # store in global if correct
        g.user = user_data
        return f(*args, **kwargs)
    return decorated_function

