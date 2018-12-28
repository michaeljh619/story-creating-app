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

@app.route('/categories/')
def showCategories():
    # get categories from database
    session = create_session()
    categories = session.query(Category).all()
    # close database session
    session.close()
    # get user if logged in
    user = get_user()
    return render_template("categories.html",
                           categories=categories,
                           user=user)
