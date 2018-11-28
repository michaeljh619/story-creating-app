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

# edit story page
@app.route('/categories/<int:category_id>/story/<int:story_id>'
           + '/page/edit/<int:page_id>',
           methods=['GET', 'POST'])
def editStoryPage(category_id, story_id, page_id):
    # start an sql session
    session = create_session()
    # get category
    category = session.query(Category).get(category_id)
    # get story
    story = session.query(Story).get(story_id)
    # get page
    page = session.query(Story_Page).get(page_id)
    # post
    if request.method == 'POST':
        # edit the page
        page.name = request.form['name']
        page.description = request.form['description']
        page.text = request.form['text']
        # add and commit
        session.add(page)
        session.commit()
        # close session
        session.close()
        return redirect(url_for("editPages",
                                category_id=category_id,
                                story_id=story_id))
    else:
        session.close()
        return render_template("editStoryPage.html",
                               category=category,
                               story=story,
                               page=page)
