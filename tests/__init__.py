"""Initial configuration for the tests"""
from cime_mirror_engine.app import app, db
from cime_mirror_engine.config import Test
from cime_mirror_engine.models import User

#Configuration is changed for testing
app.config.from_object(Test)
# Testing client is generated
client = app.test_client()
# Database schema is executed in the 'new' database
db.create_all()

#TODO change this for a generate_super_user() function
test_user = User('1234')
db.session.add(test_user)
db.session.commit()
response = client.post(
    '/auth/login',
    data={'pin' : '1234'},
)

################################
### TEST USER AUTHENTICATION ###
################################
def test_login_logout():
    """Tests user login and logout auth"""
    #TODO add tests for unauthorized requests here and in Resources
    invalid_login = client.post(
        '/auth/login',
        data={'pin' : '4321'},
    )
    login_response = client.post(
        '/auth/login',
        data={'pin' : '1234'},
    )
    assert invalid_login.data == "'Invalid Pin'\n"
    assert login_response.data == "'Logged in successfully'\n"
    logout_response = client.get('/auth/login')
    assert logout_response.data == "'Logged Out Successfully'\n"
