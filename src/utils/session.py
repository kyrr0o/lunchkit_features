"""
Session Management Utility Module
-------------------------------

This module provides session initialization functionality for user authentication, 
creating and managing user sessions with security features.

Key Components:
    - UUID-based session ID generation
    - Configurable session expiration
    - IP address and user agent tracking
    - Timestamp management
    - Integration with Session model

Functions:
    - init_session(user_data): Creates new session with user data
        Parameters:
            - user_data: Dictionary containing authenticated user information
        Returns:
            - session_id: Unique identifier for the created session


Usage Example:
    session_id = init_session({
        'user_id': 123,
        'email': 'user@example.com',
        'role': 'store_owner'
    })
"""





from src.models.Session import Session
from flask import current_app,request

import uuid
from datetime import datetime, timedelta, timezone

# Creates the sesion with the user data
def init_session(user_data):
    session_id = str(uuid.uuid4())
    created_at = datetime.now()
    print('Item is created today with date: ',created_at)
    expires_at = created_at + current_app.config['PERMANENT_SESSION_LIFETIME']
    
    Session.save_session(
        session_id=session_id,
        user_data=user_data,
        expires_at=expires_at,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    return session_id