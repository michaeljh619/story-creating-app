#!/usr/bin/python

# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story, Story_Page, Page_Link

# flask app
app = Flask(__name__)

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

# function to create app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # test config
    if test_config is None:
        # load instance config, if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
