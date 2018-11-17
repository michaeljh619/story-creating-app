#!/usr/bin/python

# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story, Story_Page, Page_Link

# flask app
app = Flask(__name__)


# sql session creation
def create_session():
    engine = create_engine('sqlite:///stories.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


# main page showing all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    # get categories from database
    session = create_session()
    categories = session.query(Category).all()
    # close database session
    session.close()
    return render_template("categories.html", categories=categories)


# show all stories under a category
@app.route('/categories/<int:category_id>/')
def showCategory(category_id):
    # start sql session
    session = create_session()
    # get category and check it's valid
    category = session.query(Category).get(category_id)
    if not category:
        return None
    # get stories
    stories = session.query(Story).filter_by(category_id=category.id)
    # close database session
    session.close()
    return render_template("showCategory.html",
                           category=category,
                           stories=stories)


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
    print(str(story_id))
    if not story:
        return None
    # get root page if a page is not specified
    page = None
    print(str(page_id))
    if page_id == 0:
        page = session.query(
            Story_Page).filter_by(is_root=True,
                                  story_id=story.id).one()
    # page was specified
    else:
        page = session.query(Story_Page).get(page_id)
    # check page is valid
    if not page:
        return None
    # get linked pages
    page_links = session.query(Page_Link).filter_by(
                    base_page_id=page.id).all()
    linked_pages = []
    for page_link in page_links:
        linked_page = session.query(Story_Page).get(
                        page_link.linked_page_id)
        linked_pages.append(linked_page)
        print(linked_page.name)
    # close sql session
    session.close()
    return render_template("showStory.html",
                           category=category,
                           story=story,
                           page=page,
                           linked_pages=linked_pages)


# new story page
@app.route('/categories/<int:category_id>/story/new')
def newStory(category_id):
    return render_template("newStory.html")


# edit story page
@app.route('/story/<int:story_id>/edit')
def editStory(story_id):
    return render_template("editStory.html")


# delete story page
@app.route('/story/<int:story_id>/delete')
def deleteStory(story_id):
    return render_template("deleteStory.html")


# if main
if __name__ == '__main__':
    # allows code update w/o server restart
    app.debug = True
    # listen on all addresses
    app.run(host='0.0.0.0', port=5000)
