# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story
from database_setup import Story_Page, Page_Link
from storyApp import app

# sql session creation
def create_session():
    engine = create_engine('sqlite:///stories.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

# show all stories under a category
@app.route('/categories/<int:category_id>/')
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
    return render_template("showCategory.html",
                           category=category,
                           stories=stories)
