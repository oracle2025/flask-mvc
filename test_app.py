import pytest
from app import app, init_db
import os
import tempfile


@pytest.fixture
def tester():
    return app.test_client()

def test_index(tester):
    '''the app :: the index page :: ensure it is 404'''
    response = tester.get('/', content_type='html/text')
    assert response.status_code == 200

def test_database(tester):
    '''the database :: database file :: ensure it exists'''
    assert os.path.exists("flaskr.db") == True

@pytest.fixture(scope='module')
def tester_db(request):
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    tester = app.test_client()
    init_db()
    def tester_db_teardown():
        os.close(db_fd)
        os.unlink(app.config['DATABASE'])
    request.addfinalizer(tester_db_teardown())
    return tester

def test_empty_db(tester_db):
    """the database :: initial database :: ensure it is empty"""
    rv = tester_db.get('/')
    assert b'No entries yet. Add some!' in rv.data

class TestClass:
    """the database :: initial database :: ensure it is empty"""
    def setup_class(self):
        """Set up a blank temp database before each test"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        init_db()

    def tteardown_class(self):
        """Destroy blank temp database after each test"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        """the database :: initial database :: ensure it is empty"""
        rv = self.app.get('/')
        assert b'No entries yet. Add some!' in rv.data

    def ttest_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login(
            app.config['USERNAME'],
            app.config['PASSWORD']
        )
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(
            app.config['USERNAME'] + 'x',
            app.config['PASSWORD']
        )
        assert b'Invalid username' in rv.data
        rv = self.login(
            app.config['USERNAME'],
            app.config['PASSWORD'] + 'x'
        )
        assert b'Invalid password' in rv.data

    def ttest_messages(self):
        """Ensure that user can post messages"""
        self.login(
            app.config['USERNAME'],
            app.config['PASSWORD']
        )
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data





