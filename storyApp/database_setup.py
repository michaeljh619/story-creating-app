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
# turn on to reset database and fill with test data
FILL_DB_WITH_TEST_DATA = False

# Create base class for sql tables
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    # user info
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=True)
    avatar = Column(String(200))
    
    # login
    active = Column(Boolean, default=False)
    tokens = Column(Text)


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
            'id': self.id,
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

    owner_id = Column(Integer,
                     ForeignKey('user.id'))
    owner = relationship(User)

    @property
    def serialize(self):
        # returns object data in serializeable format
        return{
            'name': self.name,
            'id': self.id,
            'description': self.description,
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

    @property
    def serialize(self):
        # returns object data in serializeable format
        return{
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'text': self.text,
            'is_root': self.is_root,
        }


class Page_Link(Base):
    __tablename__ = 'page_link'
    id = Column(Integer, primary_key=True)

    # linked page ids
    base_page_id = Column(Integer, ForeignKey('story_page.id'))
    linked_page_id = Column(Integer, ForeignKey('story_page.id'))

    # linked pages
    base_page = relationship(Story_Page, 
                             foreign_keys=[base_page_id])
    linked_page = relationship(Story_Page,
                               foreign_keys=[linked_page_id])

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
if FILL_DB_WITH_TEST_DATA:
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
    session.query(User).delete()
    session.commit()
    
    # create categories
    categories = [ Category(name="Action"),
                Category(name="Adventure"),
                Category(name="Horror") ]
    for c in categories:
        session.add(c)
        session.commit()
    
    '''
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
    page1_link_a = Page_Link(base_page=story1_page1,
                            linked_page=story1_page2a,
                            story=story1)
    page1_link_b = Page_Link(base_page=story1_page1,
                            linked_page=story1_page2b,
                            story=story1)
    session.add(page1_link_a)
    session.add(page1_link_b)
    session.commit()
    '''
    # close database
    session.close()
