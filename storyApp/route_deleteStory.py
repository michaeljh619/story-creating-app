# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story
from database_setup import Story_Page, Page_Link
from storyApp import app
from db_session import create_session

# delete story
@app.route('/categories/<int:category_id>/story' 
           + '/<int:story_id>/delete',
           methods=['GET', 'POST'])
def deleteStory(category_id, story_id):
    # start sql session
    session = create_session()
    # get category
    category = session.query(Category).get(category_id)
    cat_id = category.id
    # get story
    story = session.query(Story).get(story_id)
    if request.method == 'POST':
        # delete all page links associated with story
        session.query(Page_Link).filter_by(
                story_id=story.id).delete()
        # delete all pages associated with story
        session.query(Story_Page).filter_by(
                story_id=story.id).delete()
        # delete story
        session.query(Story).filter_by(
                id=story.id).delete()

        # close session and redirect
        session.commit()
        session.close()
        return redirect(url_for('showCategory',
                        category_id=category_id))
    else:
        # close session
        session.close()
        return render_template("deleteStory.html",
                           story=story,
                           category=category)
