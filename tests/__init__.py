"""Initial configuration for the tests"""
from cime_mirror_engine.app import app, db
from cime_mirror_engine.config import Test
from cime_mirror_engine.models import User
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
