#!/usr/bin/python

# imports
from flask import Flask, render_template, request, session
from flask import redirect, url_for, jsonify
from flask_oauthlib.client import OAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story, Story_Page, Page_Link

# flask app
app = Flask(__name__)
app.secret_key = "development"

# Google OAuth
GOOGLE_ID = ('437774503588-h4oksfqj6p99qanoo'
                            '32nde0qjroo6107'
                            '.apps.googleusercontent.com')
GOOGLE_SECRET = '-FGtgnVG3MIzfUlfic0joUAc'
oauth = OAuth(app)
google = oauth.remote_app('google',
    consumer_key=GOOGLE_ID,
    consumer_secret=GOOGLE_SECRET,
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# route imports
import storyApp.route_home

import storyApp.route_showCategories
import storyApp.route_showCategory
import storyApp.route_showStory
import storyApp.route_newStory
import storyApp.route_editStory
import storyApp.route_deleteStory
import storyApp.route_editPages
import storyApp.route_addPage
import storyApp.route_editPage
import storyApp.route_deletePage
import storyApp.route_login
import storyApp.route_authorized

from google_oauth import GoogleAuth


# function to create app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # test config
    #if test_config is None:
        # load instance config, if exists, when not testing
        #app.config.from_pyfile('config.py', silent=True)
    #else:
        # load test config if passed in
        #app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
