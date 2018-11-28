#!/usr/bin/python

# imports
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import sys

'''
Script designed to set up an SQL database
using SQLAlchemy.
'''

# Create base class for sql tables
Base = declarative_base()


# Create Restaurant Class (table)
class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80),
                  nullable=False)
    id = Column(Integer,
                primary_key=True)

    @property
    def serialize(self):
        return{
            'name': self.name,
        }


# Create Menu Item Class (table)
class Story(Base):
    __tablename__ = 'story'
    name = Column(String(80),
                  nullable=False)
    id = Column(Integer,
                primary_key=True)

    description = Column(String(250))

    category_id = Column(Integer,
                         ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        # returns object data in serializeable format
        return{
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'category': self.category,
        }


class Story_Page(Base):
    __tablename__ = 'story_page'
    name = Column(String(80),
                  nullable=False)
    id = Column(Integer,
                primary_key=True)

    # story description and text
    description = Column(String(250))
    text = Column(Text())

    # is the root page link
    is_root = Column(Boolean())

    # linkage to story
    story_id = Column(Integer,
                      ForeignKey('story.id'))
    story = relationship(Story)


class Page_Link(Base):
    __tablename__ = 'page_link'
    id = Column(Integer, primary_key=True)

    base_page_id = Column(Integer)
    linked_page_id = Column(Integer)

    # linkage to story
    story_id = Column(Integer,
                      ForeignKey('story.id'))
    story = relationship(Story)



# Sql Database setup footer
engine = create_engine(
    'sqlite:///stories.db')

Base.metadata.create_all(engine)


'''
Fills Database with stuff
'''
# set up session
engine = create_engine('sqlite:///stories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# clear database
session.query(Category).delete()
session.query(Story).delete()
session.query(Story_Page).delete()
session.query(Page_Link).delete()
session.commit()

# create categories
categories = [ Category(name="Action"),
               Category(name="Adventure"),
               Category(name="Horror") ]
for c in categories:
    session.add(c)
    session.commit()

# create stories
story1 = Story(name="Action Jack",
               description="Explosions, car chases, and action!",
               category=categories[0])
story2 = Story(name="Action Phil",
               description="Action Jack's brother, not as cool.",
               category=categories[0])
story3 = Story(name="The Mage's Path",
               description="Wield magic in a medieval realm!",
               category=categories[1])
story4 = Story(name="Lost in the Woods",
               description="You are lost in a forest, but not alone...",
               category=categories[2])
session.add(story1)
session.add(story2)
session.add(story3)
session.add(story4)

# create story pages
story1_page1 = Story_Page(name="Start Story",
                          description="Action Jack in a car chase",
                          text="Action Jack is being chased in a car!",
                          story=story1,
                          is_root=True)
story1_page2a = Story_Page(name="Hit the brakes",
                          description="Action Jack hits the brakes", 
                          text="He hits the brakes and the baddies zoom by",
                          story=story1,
                          is_root=False)
story1_page2b = Story_Page(name="Hit the gas",
                          description="Action Jack slams the gas", 
                          text="He floors it and gets away!",
                          story=story1,
                          is_root=False)
session.add(story1_page1)
session.add(story1_page2a)
session.add(story1_page2b)
session.commit()

# create page links
page1_link_a = Page_Link(base_page_id=story1_page1.id,
                         linked_page_id=story1_page2a.id,
                         story=story1)
page1_link_b = Page_Link(base_page_id=story1_page1.id,
                         linked_page_id=story1_page2b.id,
                         story=story1)
session.add(page1_link_a)
session.add(page1_link_b)
session.commit()

# close database
session.close()
