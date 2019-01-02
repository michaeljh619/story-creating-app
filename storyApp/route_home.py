# imports
from flask import Flask, render_template, request, session
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story, User
from database_setup import Story_Page, Page_Link
from storyApp import app, google
from db_session import create_session
from google_helper import get_user
import routes

# show all stories under a category
@app.route(routes.ROUTES['showHome_route'])
def showHome():
    user = get_user()
    return render_template("home.html", user=user)
