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

@app.route('/')
@app.route('/categories/')
def showCategories():
    # get categories from database
    session = create_session()
    categories = session.query(Category).all()
    # close database session
    session.close()
    return render_template("categories.html", categories=categories)
