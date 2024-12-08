"""

    Cloudinary Configuration Module
    ---------------------
    This module loads environment variables from a .env file 
    to manage application settings for cloudinary. 

"""
import os
import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    secure=True
)