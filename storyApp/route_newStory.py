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

# new story
@app.route('/categories/story/new',
           methods=['GET','POST'])
def newStory():
    # start sql session
    session = create_session()
    # get categories
    categories = session.query(Category).all()
    # if submitted form
    if request.method == 'POST':
        # get category that the story is being posted to
        category_id= request.form['category']
        # create new story
        story = Story(name=request.form['name'],
                      description=request.form['description'],
                      category_id=category_id)
        session.add(story)
        # close sql session
        session.commit()
        session.close()
        return redirect(url_for('showCategory',
                                category_id=category_id))
    else:
        # close sql session
        session.close()
        return render_template("newStory.html", 
                               categories=categories)
