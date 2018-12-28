from database_setup import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# sql session creation
def create_session():
    engine = create_engine('sqlite:///stories.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
