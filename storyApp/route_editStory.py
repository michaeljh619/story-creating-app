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

# edit story
@app.route('/categories/<int:category_id>/story/<int:story_id>/edit',
           methods=['GET', 'POST'])
def editStory(category_id, story_id):
    # start sql session
    session = create_session()
    # get category
    category = session.query(Category).get(category_id)
    cat_id = category.id
    # get story
    story = session.query(Story).get(story_id)
    if request.method == 'POST':
        story.name = request.form['name']
        story.description = request.form['description']
        session.add(story)
        session.commit()
        # close sql session and redirect
        session.close()
        return redirect(url_for('showCategory',
                                category_id=cat_id))
    else:
        # close sql session
        session.close()
        user = get_user()
        return render_template("editStory.html",
                           category=category,
                           story=story,
                           user=user)
