# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story
from database_setup import Story_Page, Page_Link
from storyApp import app, google
from db_session import create_session
import routes

# show all stories under a category
@app.route(routes.ROUTES['login_route'])
def login():
    return google.authorize(
                callback=url_for('authorized', _external=True))
