# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story
from database_setup import Story_Page, Page_Link
from storyApp import app, google
from db_session import create_session
import routes

# show all stories under a category
@app.route(routes.ROUTES['logout_route'])
def logout():
    session.pop('google_token', None)
    return redirect(url_for("showHome"))
