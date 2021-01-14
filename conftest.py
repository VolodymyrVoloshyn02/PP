import pytest
import sys
from sqlalchemy.orm import close_all_sessions
sys.path.append("")


from main import engine, session as db_session, app
from models import Base, Users, db_DropEverything


@pytest.fixture(scope='function')
def testapp():
    _app = app
    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()


    yield app
    #Base("DROP TABLE authors CASCADE")
    db_DropEverything(Base)
    #Base.metadata.drop_all.cascade(bind=engine)
    #Base.metadata.drop_all(bind=engine)
    _app.connection.close()


@pytest.fixture(scope='function')
def session(testapp):
    ctx = app.app_context()
    ctx.push()

    yield db_session
    #db_session.close_all()
    close_all_sessions()
    ctx.pop()


@pytest.fixture(scope='function')
def user(session):
    user = Users(
        login="mylogin",
        password="my password",
        name="myname",
        passport="myUKRpasport",
        address="Lviv",
        email="user@gmail.com",
        phone_number="88005553535",
        status=""
    )
    session.add(user)
    session.commit()

    return user


@pytest.fixture
def client(testapp):
    return testapp.test_client()

@pytest.fixture
def user_token(user,client):
    res = client.post('/login', json={
        "login": user.login,
        "password": "my password"
    })
    return res.get_json()['access_token']

@pytest.fixture
def user_headers(user_token):
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    return headers