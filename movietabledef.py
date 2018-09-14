from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///lcp.db', echo=True)
Base = declarative_base()
 
########################################################################
class Movie(Base):
    """"""
    __tablename__ = "cities"
 
    movie_id = Column(Integer,primary_key=True)
    movie_name = Column(String)
    
    
 
    #----------------------------------------------------------------------
    def __init__(self, movie_id, movie_name):
        """"""
        self.movie_id = movie_id
        self.movie_name = movie_name

 
# create tables
Base.metadata.create_all(engine)