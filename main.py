#!/usr/bin/python

# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# flask app
app = Flask(__name__)


# main page showing all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    return render_template("categories.html")


# show all stories under a category
@app.route('/categories/<string:category>/')
def showCategory(category):
    return render_template("showCategory.html",
                           category=category)


# show a particular story in a category
@app.route('/categories/<string:category>/story/<int:story_id>')
def showStory(category, story_id):
    return render_template("showStory.html")


# new story page
@app.route('/categories/<string:category>/story/new')
def newStory(cat_id):
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
