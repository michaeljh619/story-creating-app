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
import routes

# delete story page
@app.route(routes.ROUTES['deleteStoryPage_route'],
           methods=['GET', 'POST'])
def deleteStoryPage(category_id, story_id, page_id):
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
        # delete and commit
        session.query(Story_Page).filter_by(id=page_id).delete()
        session.query(Page_Link).filter_by(
                        linked_page_id=page_id).delete()
        session.query(Page_Link).filter_by(
                        base_page_id=page_id).delete()
        session.commit()
        # close session
        session.close()
        return redirect(url_for("editPages",
                                category_id=category_id,
                                story_id=story_id))
    else:
        session.close()
        user = get_user()
        return render_template("deleteStoryPage.html",
                               category=category,
                               story=story,
                               page=page,
                               user=user)
