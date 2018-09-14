from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///lcp.db', echo=True)
Base = declarative_base()
 
########################################################################
class City(Base):
    """"""
    __tablename__ = "cities"
 
    city_id = Column(Integer,primary_key=True)
    city_name = Column(String)
    
    
 
    #----------------------------------------------------------------------
    def __init__(self, city_id, city_name):
        """"""
        self.city_id = city_id
        self.city_name = city_name

 
# create tables
Base.metadata.create_all(engine)