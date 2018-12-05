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


def create_page_tree(page, parent, depth):
    # get all page links
    session = create_session()
    # get all linked pages
    linked_pages = session.query(Story_Page).     \
            filter(Story_Page.id==Page_Link.linked_page_id). \
            filter(Page_Link.base_page_id==page.id).         \
            all()
    linked_pages_trees = []
    session.close()
    # create array of page trees (occurs if not a leaf)
    for linked_page in linked_pages:
        linked_page_tree = create_page_tree(linked_page,
                                            page, depth+1)
        linked_pages_trees.append(linked_page_tree)
    # return page tree
    return (page, linked_pages_trees, parent, depth)
    

# pick a page to add a linked page to
@app.route('/categories/<int:category_id>/story/'
           + '<int:story_id>/pages')
def editPages(category_id, story_id):
    # start an sql session
    session = create_session()
    # get category
    category = session.query(Category).get(category_id)
    # get story
    story = session.query(Story).get(story_id)
    # get list of pages
    pages = session.query(Story_Page).filter_by(
                story_id=story.id).all()
    # close session
    session.close()
    if len(pages) == 0:
        # redirect
        return redirect(url_for("addStoryPage",
                                category_id=category_id,
                                story_id=story_id,
                                linking_page_id=0))
    else:
        # get root page
        session = create_session()
        root_page = session.query(Story_Page).filter_by(
                story_id=story.id,
                is_root=True).one()
        session.close()
        # create page tree
        page_tree = [create_page_tree(root_page, None, 0)]
        return render_template("editPages.html",
                               story=story,
                               category=category,
                               page_tree=page_tree)
