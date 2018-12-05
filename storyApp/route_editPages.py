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
    page_links = session.query(Page_Link).filter_by(
                base_page_id=page.id).all()
    # get all linked pages
    linked_pages = []
    linked_pages_trees = []
    # in a branch (has linked pages)
    if len(page_links) > 0:
        # create array of pages
        for page_link in page_links:
            # query linked page
            linked_page = session.query(Story_Page).get(
                            page_link.linked_page_id)
            linked_pages.append(linked_page)
        # close session
        session.close()
        # create array of page trees
        for linked_page in linked_pages:
            linked_page_tree = create_page_tree(linked_page,
                                                page, depth+1)
            linked_pages_trees.append(linked_page_tree)
    # in a leaf (no linked pages)
    else:
        session.close()
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
