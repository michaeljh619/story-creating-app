# imports
from flask import Flask, render_template, request, abort
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Story
from database_setup import Story_Page, Page_Link
from storyApp import app
from db_session import create_session
from google_helper import get_user
import routes

# add story page
@app.route(routes.ROUTES['addStoryPage_route'],
           methods=['GET', 'POST'])
def addStoryPage(category_id, story_id, linking_page_id):
    user = get_user()
    # start an sql session
    session = create_session()
    # get category
    category = session.query(Category).get(category_id)
    # get story
    story = session.query(Story).get(story_id)
    # Protect this page by login
    if user == None:
        return redirect(url_for("login"))
    owner = story.owner
    if user.id != owner.id:
        return abort(401)
    # get linking_page
    linking_page = None
    if linking_page_id != 0:
        linking_page = session.query(Story_Page).get(linking_page_id)
    # post
    if request.method == 'POST':
        # check if root
        is_root = False
        if linking_page_id == 0:
            is_root = True
        # create the page
        page = Story_Page(name=request.form['name'],
                          description=request.form['description'],
                          text=request.form['text'],
                          is_root=is_root,
                          story_id=story.id)
        session.add(page)
        session.commit()
        # create a page link if not root
        if not is_root:
            page_link = Page_Link(base_page_id=linking_page_id,
                                  linked_page_id=page.id,
                                  story_id=story.id)
            session.add(page_link)
            session.commit()
        # close session
        session.close()
        return redirect(url_for("editPages",
                                category_id=category_id,
                                story_id=story_id))
    else:
        session.close()
        return render_template("newStoryPage.html",
                               category=category,
                               story=story,
                               linking_page=linking_page,
                               user=user)
