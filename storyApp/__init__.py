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
