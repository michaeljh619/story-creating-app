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

@app.route(routes.ROUTES['showCategoryJSON_route'])
def showCategoryJSON(category_id):
    # start sql session
    session = create_session()
    # get category and check it's valid
    category = session.query(Category).get(category_id)
    if not category:
        return None
    # get stories
    stories = session.query(Story).filter_by(
            category_id=category.id)
    # close database session
    session.close()
    # return JSON file of categories
    return jsonify(Stories=[s.serialize for s in stories])
