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
    linked_pages = None
    if page:
        page_links = session.query(Page_Link).filter_by(
                    base_page_id=page.id).all()
        linked_pages = []
        for page_link in page_links:
            linked_page = session.query(Story_Page).get(
                            page_link.linked_page_id)
            linked_pages.append(linked_page)
    # close sql session
    session.close()
    return render_template("showStory.html",
                           category=category,
                           story=story,
                           page=page,
                           linked_pages=linked_pages)


# new story page
@app.route('/categories/<int:category_id>/story/new',
           methods=['GET','POST'])
def newStory(category_id):
    # start sql session
    session = create_session()
    # get category
    category = session.query(Category).get(category_id)
    cat_id = category.id
    if not category:
        session.close()
        return None
    # if submitted form
    if request.method == 'POST':
        # create new story
        story = Story(name=request.form['name'],
                      description=request.form['description'],
                      category_id=category.id)
        session.add(story)
        # close sql session
        session.commit()
        session.close()
        return redirect(url_for('showCategory',
                                category_id=cat_id))
    else:
        # close sql session
        session.close()
        return render_template("newStory.html",
                               category=category)


# edit story page
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
        return render_template("editStory.html",
                           category=category,
                           story=story)


# delete story page
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
        # delete story
        session.delete(story)
        # delete all pages associated with story
        # delete all page links associated with story
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


# if main
if __name__ == '__main__':
    # allows code update w/o server restart
    app.debug = True
    # listen on all addresses
    app.run(host='0.0.0.0', port=5000)
