#!/usr/bin/python

# imports
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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

