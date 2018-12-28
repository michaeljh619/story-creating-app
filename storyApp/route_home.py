# imports
from flask import Flask, render_template, request, session
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story, User
from database_setup import Story_Page, Page_Link
from storyApp import app, google
from db_session import create_session

# show all stories under a category
@app.route('/')
def showHome():
    user = None
    if 'google_token' in session:
        g_user = google.get('userinfo')
        db_session = create_session()
        user = db_session.query(User).filter_by(
                email=g_user.data['email']).one()
        db_session.close()
    return render_template("home.html", user=user)
