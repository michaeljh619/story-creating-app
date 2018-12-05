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

# show a particular story in a category
@app.route('/categories/<int:category_id>/story/<int:story_id>/page/<int:page_id>')
def showStory(category_id, story_id, page_id):
    # start sql session
    session = create_session()
    # get category
    category = session.query(Story).get(category_id)
    if not category:
        return None
    # get story
    story = session.query(Story).get(story_id)
    if not story:
        return None
    # get root page if a page is not specified
    page = None
    if page_id == 0:
        page_query = session.query(
            Story_Page).filter_by(is_root=True,
                                  story_id=story.id)
        if page_query.count() > 0:
            page = page_query.one()
    # page was specified
    else:
        page = session.query(Story_Page).get(page_id)
    # get linked pages
    linked_pages = session.query(Story_Page).     \
            filter(Story_Page.id==Page_Link.linked_page_id). \
            filter(Page_Link.base_page_id==page.id).         \
            all()
    # close sql session
    session.close()
    return render_template("showStory.html",
                           category=category,
                           story=story,
                           page=page,
                           linked_pages=linked_pages)
