"""Initial configuration for the tests"""
from web_app.app import app, db
from web_app.config import Test
from web_app.models import User
from run import create_superuser

#Configuration is changed for testing
app.config.from_object(Test)
# Testing client is generated
client = app.test_client()
# Database schema is executed in the 'new' database
db.create_all()
# Create Super User
create_superuser()
# Log In in case other tests are run before auth tests.
# Since those ones are supposed to perform the login.
response = client.post(
    '/auth/login/',
    data={'pin' : '1234'},
)
