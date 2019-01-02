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

# show all stories under a category
@app.route(routes.ROUTES['showCategory_route'])
def showCategory(category_id):
    # start sql session
    session = create_session()
    # get category and check it's valid
    category = session.query(Category).get(category_id)
    if not category:
        return None
    # get stories
    stories = session.query(Story).filter_by(category_id=category.id)
    # close database session
    session.close()
    # get user if logged in
    user = get_user()
    return render_template("showCategory.html",
                           category=category,
                           stories=stories,
                           user=user)
