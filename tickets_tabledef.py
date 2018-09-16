from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///login.db', echo=True)
Base = declarative_base()
 
########################################################################
class Ticket(Base):
    """"""
    __tablename__ = "tickets"
 	
    ticket_id = Column(Integer,primary_key=True)
    username = Column(String)
    city_name = Column(String)
    theatre_name = Column(String)
    movie_name = Column(String)
    show_time = Column(String)
        
 
    #----------------------------------------------------------------------
    def __init__(self, ticket_id, username, city_name, theatre_name, movie_name,  show_time):

        self.ticket_id = ticket_id
        self.username = username
        self.city_name = city_name
        self.theatre_name = theatre_name
        self.movie_name = movie_name
        self.show_time = show_time
        

 
# create tables
Base.metadata.create_all(engine)