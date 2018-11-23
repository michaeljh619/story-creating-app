#!/usr/bin/python

# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# database tables
from database_setup import Base, Category, Story, Story_Page, Page_Link

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
