from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///login.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """
    Define the user table to store the
    logging information
    """
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    phno = Column(String)
    
 
    #----------------------------------------------------------------------
    def __init__(self, username, password, phno):
        """"""
        self.username = username
        self.password = password
        self.phno = phno

 
# creates the table from the schema provided
Base.metadata.create_all(engine)
