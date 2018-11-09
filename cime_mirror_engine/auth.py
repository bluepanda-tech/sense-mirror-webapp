"""This file handle user authentications"""
from flask import request
from flask_restful import Resource
from flask_login import (
    login_user,
    logout_user,
)

from .app import (
    app,
    api,
    login,
)
from .models import User

@login.user_loader
def load_user(user_id):
    """This extension expects that the application will
     configure a user loader function, that can be called to
     load a user given the ID.

      Each time the logged-in user navigates to a new page,
      Flask-Login retrieves the ID of the user from the session,
      and then loads that user into memory.

      The id that Flask-Login passes to the function as an
      argument is going to be a string, so a proper convertion
      is needed."""
    try:
        return User.query.get(int(user_id))
    except:
        return None

class LogIn(Resource):
    """Endopint to LogIn using the user's PIN"""
    def post(self):
        """User authentication & validation"""
        #TODO add error handler in here
        user = User.query.first() # Only one superuser
        pin = request.form['pin'] # Get PIN from form
        if not user.check_password(pin): # Validate PIN
            return 'Invalid Pin'
        login_user(user)
        return 'Logged in successfully'
api.add_resource(LogIn, '/auth/login')

class LogOut(Resource):
    """Endopint to LogOut the user"""
    def get(self):
        #TODO validation to check if user is actually logged in
        logout_user()
        return "Logged Out Successfully"
api.add_resource(LogOut, '/auth/logout')
