# imports
from flask import Flask, render_template, request, session
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story
from database_setup import Story_Page, Page_Link, User
from storyApp import app, google

# sql session creation
def create_session():
    engine = create_engine('sqlite:///stories.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def create_new_user(g_user, db_session):
    user = User(email=g_user.data['email'], 
                name=g_user.data['name'],
                avatar=g_user.data['picture'])
    db_session.add(user)
    db_session.commit()
    return None

# show all stories under a category
@app.route('/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    # get user info
    g_user = google.get('userinfo')
    # if user not in database, create new user
    db_session = create_session()
    user_query = db_session.query(User).filter_by(
            email=g_user.data['email']).all()
    if len(user_query) == 0:
        create_new_user(g_user, db_session)
    # close db session
    db_session.close()
    return redirect(url_for("showHome"))
    #return jsonify({"data": me.data})
