from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, current_app, make_response, g
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests
import json
from src.models.Session import Session
from src.models import User, Session, Item
from src.utils import init_session
from src.routes.auth.StoreOwnerRoutes import login_required_owner
from src.models.Store import Store
from src.models.storeApplication import StoreApplication
from src.forms.StoreOwner.NewItem import AddItem


from cloudinary import CloudinaryImage
from cloudinary.uploader import upload


store_bp = Blueprint('store-admin',__name__)


@store_bp.route('/dashboard')
@login_required_owner
def storeAdminDashboard():
    form = AddItem()
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect(url_for('auth.ownerLogin'))
            
    session_data = Session.get_session(session_id)
    userData = session_data['user_data']
    ownerId = userData['owner_id']
    return render_template('store/storeAdminDashboard.html', ownerId=ownerId)

#This route displays all the items of a registered store.
@store_bp.route('storecontents/<string:StoreOwnerId>', methods=['GET', 'POST'])
@login_required_owner
def storecontents(StoreOwnerId):
    form = AddItem()
    if request.method == "GET":
        print(StoreOwnerId)
        storeDetails = Store.get_store_details(StoreOwnerId) #This fetches the dynamically routed Store.
        print(storeDetails['StoreId'])
        StoreItems = Item.get_storeItems(storeDetails['StoreId']) #This fetches the Store Items.
        print(StoreItems)
    return render_template ('store/storecontents.html', storeDetails=storeDetails, form = form, 
                            StoreItems = StoreItems, StoreId = storeDetails['StoreId'])

#This route displays all the items of a registered store.
@store_bp.route('storecontents/pending/<string:StoreOwnerId>', methods=['GET', 'POST'])
def storecontentsPending(StoreOwnerId):
    if request.method == "GET":
        storeOwner = StoreApplication.getLatestApplication(StoreOwnerId)
        if(storeOwner['ApplicationStatus'] == 'Pending'):
            isPending = True
        else:
            isPending = False
        return render_template ('store/storecontentsPending.html',isPending=isPending)


@store_bp.route('storeorders/<string:StoreOwnerId>', methods=['GET', 'POST'])
@login_required_owner
def storeorders(StoreOwnerId):
    storeDetails = Store.get_store_details(StoreOwnerId)
    return render_template ('store/storeorders.html', storeDetails=storeDetails)

# Logout handler
@store_bp.route('/logout-store')
def logoutStore():
    session_id = request.cookies.get('session_id')
    if session_id:
        Session.delete_session(session_id)
    
    response = make_response(redirect(url_for('auth.ownerLogin')))
    response.delete_cookie('session_id')
    return response


@store_bp.route('/store/add-item', methods=['POST'])
def add_item():
    form = AddItem()
    if request.method == 'POST' and form.is_submitted():

        session_id = request.cookies.get('session_id')
        session_data = Session.get_session(session_id)
        user_data = json.loads(session_data['user_data'])
        store_owner_id = user_data['owner_id'] 

        itemName = form.itemName.data
        itemDesc = form.itemDesc.data
        itemPrice = form.itemPrice.data
        itemPhoto = form.itemPhoto.data
        StoreId = form.StoreId.data
        print(StoreId)
        
        uploaded_file = upload(itemPhoto)
        Image = CloudinaryImage(uploaded_file['public_id']).build_url(width = 100, height = 50, crop = "fill")
                
        new_item = Item.add_item(itemName, itemDesc, itemPrice, Image, StoreId)
        print(new_item)
        return redirect(url_for('store-admin.storecontents', StoreOwnerId = store_owner_id))


@store_bp.route('/visit-store/<string:storeId>', methods=['GET'])  # matches your URL parameter
def visitStore(storeId):    # matches your function parameter
    storeDetails = Store.get_store_details_storeId(storeId)
    items = Item.get_storeItems(storeId)
    return render_template('user/storeHomepage.html',
                         storeDetails=storeDetails,
                         items=items)


