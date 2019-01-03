import os
import tempfile
import pytest
from storyApp import storyApp
import storyApp.routes as routes
from storyApp.db_session import create_session
from storyApp.database_setup import Base, Category, User
from storyApp.database_setup import Story, Story_Page, Page_Link

@pytest.fixture
def client():
    db_fd, storyApp.app.config['DATABASE'] = tempfile.mkstemp()
    storyApp.app.config['TESTING'] = True
    client = storyApp.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(storyApp.app.config['DATABASE'])

def test_routes(client):
    # Debug print
    print()
    print("---- Testing Routes ---")

    # Run through all routes
    for key in routes.ROUTES:
        # Skip certain routes
        if key == "authorized_route":
            continue

        # Test all other routes
        print("Testing: " + key)
        # assert route names are valid
        assert "/" in routes.ROUTES[key]
        # ensure accessing a route does not cause error
        rv = client.get(routes.ROUTES[key])

    # Debug Print
    print("---- Testing Routes Complete ---")

def test_database(client):
    # Debug print
    print()
    print("---- Testing Database ---")

    """
    Check that the correct tables exist
    """
    table_names = Base.metadata.tables.keys()
    assert 'category' in table_names
    assert 'story' in table_names
    assert 'user' in table_names
    assert 'story_page' in table_names
    assert 'page_link' in table_names

    """
    Open and close a session to db
    """
    session = create_session()
    session.close()

    """
    Test that data can be written to a category
    """
    session = create_session()
    # Add new test category
    test_category = Category(name="Test Category")
    session.add(test_category)
    session.commit()
    # Check Object exists in db
    query_list = session.query(Category).filter_by(
                                name="Test Category").all()
    assert len(query_list) == 1
    # Delete Object
    session.query(Category).filter_by(name="Test Category").delete()
    session.commit()
    # Check Object does not exist in db
    query_list = session.query(Category).filter_by(
                                name="Test Category").all()
    assert len(query_list) == 0
    # close
    session.close()


    # Debug print
    print("---- Testing Database Complete ---")

