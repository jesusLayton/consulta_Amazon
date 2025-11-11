# Configuration settings for the Flask application

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    # Database configuration (if applicable)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///your_database.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Add any other configuration variables you need
    # For example, API keys, timeout settings, etc.