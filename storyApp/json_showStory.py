# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story
from database_setup import Story_Page, Page_Link
from storyApp import app
from db_session import create_session
from google_helper import get_user
import routes

# show a particular story in a category
@app.route(routes.ROUTES['showStoryJSON_route'])
def showStoryJSON(category_id, story_id):
    # start sql session
    session = create_session()
    # get category
    category = session.query(Story).get(category_id)
    if not category:
        return None
    # get story
    story = session.query(Story).get(story_id)
    if not story:
        return None
    # close sql session
    session.close()
    # get json
    return jsonify(Story=story.serialize,
                   Category=category.serialize)
