import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from citytabledef import *
 
engine = create_engine('sqlite:///lcp.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
city = City(101,"Delhi")
session.add(city)
 
city = City(102,"Bangalore")
session.add(city)
 
city = City(103,"Mumbai")
session.add(city)

city = City(104,"Hyderabad")
session.add(city)
 
# commit the record the database
session.commit()

session.commit()