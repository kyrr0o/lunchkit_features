"""
Store Registration Module
------------------------

This module handles the store registration process for existing store owners,
including document submission, validation, and application tracking.

Key Components:
    - Store registration form handling and validation
    - Document upload and storage via Cloudinary
    - Store application creation and management
    - Store owner verification and status updates
    - Application document tracking and storage

Routes:
    - /register-store (GET): Display store registration form with document upload fields
    - /register-store (POST): Process store registration with required documents:
        * Sanitary Permit
        * Certificate of Business Name Registration
        * Business Permit
        * Fire Safety Inspection Certificate
        * Certificate of Registration
        * Tax Payment Form
"""



from flask import render_template,jsonify,request
from .StoreOwnerRoutes import auth_bp
from src.forms.StoreOwner.RegisterStore import StoreRegistrationForm


from src.cloudinary_config import cloudinary
import cloudinary.uploader

from src.models.StoreOwner import StoreOwner
from src.models.storeApplication import StoreApplication
from src.models.applicationDocuments import ApplicationDocument

import random
import string

# Route for registration in store 
@auth_bp.route('/register-store',methods=['GET'])
def registerStore():
    form = StoreRegistrationForm()
    return render_template('auth/registerStore.html',form=form)



# Route for the actual handling of registration
@auth_bp.route('/register-store', methods=['POST'])
def register_store():
    try:
        # Validate text fields
        store_name = request.form.get('store_name')
        email = request.form.get('email')
        
        if not store_name or not email:
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400


        # Get store owner by email
        storeOwner = StoreOwner.search_storeOwner(email)
        if not storeOwner: return jsonify({'success': False, 'message':'Email has no tied storeOwner'}),401


        # Define required files for upload
        file_fields = [
            'sanitary_permit',
            'certificate_of_business_name_registration',
            'business_permit',
            'fire_safety_inspection_certificate',
            'certificate_of_registration',
            'tax_payment_form'
        ]
        
        # Container for uploaded urls of each imnage
        uploaded_urls = {}
        
        for field in file_fields:

            # Check ifthere are files missing
            if field not in request.files:
                return jsonify({
                    'success': False,
                    'message': f'Missing required file: {field}'
                }), 400
            
            # Additional checking
            file = request.files[field]
            if not file:
                return jsonify({
                    'success': False,
                    'message': f'Missing required file: {field}'
                }), 400

            try:
                # Upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder="store_registration",
                    resource_type="auto"
                )
                uploaded_urls[f"{field}_url"] = upload_result['secure_url']

            except Exception as upload_error:
                return jsonify({
                    'success': False,
                    'message': f'Failed to upload {field}'
                }), 500


        try:

             
            # Get StoreOwnerId from email
            storeOwnerId = storeOwner['StoreOwnerId']

            # Generate ApplicationId
            StoreApplicationId = generate_StoreApplicationId()

            # Create store application with Pending status using application data
            StoreApplication.create_storeApplication(StoreApplicationId,storeOwnerId,store_name,'Pending')

            # Upload the documents with the corresponding applicationId
            ApplicationDocument.create_applicationDocument(
                StoreApplicationId,
                uploaded_urls['sanitary_permit_url'],
                uploaded_urls['certificate_of_business_name_registration_url'],
                uploaded_urls['business_permit_url'],
                uploaded_urls['fire_safety_inspection_certificate_url'],
                uploaded_urls['certificate_of_registration_url'],
                uploaded_urls['tax_payment_form_url']
            )

            # Update the status of the storeOwner to Processing
            StoreOwner.update_storeOwner_application_processing(storeOwnerId)
            

            return jsonify({
                    'success': True,
                    'message': 'Please wait for Admin to verify your Registration'
                }), 200

        except Exception as e:
            return jsonify({
                    'success': False,
                    'message': f'Error has occured {str(e)}'
                }), 500
            

    except Exception as e:
        return jsonify({
                    'success': False,
                    'message': f'Error has occured {str(e)}'
                }), 500
    

# Helper function to generate random characters
def generate_StoreApplicationId():
    return ''.join(random.choices(string.ascii_letters+string.digits,k=7))


