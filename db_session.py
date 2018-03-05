import logging
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
import os
import configparser
import time

logging.basicConfig(filename="exception.log", level=logging.ERROR)
# engine = create_engine("mysql+pymysql://%s:%s@%s:%s/DBLP" % (m_username, m_password, m_address, m_port), echo=False)
config  = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__),"config.cfg"))

n_username = config.get("neo4j", "username")
n_address = config.get("neo4j", "address")
n_port = config.get("neo4j", "port")
n_password = config.get("neo4j", "password")





DB_FILE = config["data"]["db_file"]
engine=create_engine("sqlite:///%s" % DB_FILE,echo=False)


metadata = MetaData(engine)

Base = declarative_base()

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()



class Reference(Base):
    __tablename__="reference"
    article_id = Column(String(30),ForeignKey("article.id"),primary_key=True)
    citation_id = Column(String(30),ForeignKey("article.id"),primary_key=True)


class Article(Base):
    __tablename__="article"
    id = Column(String(30),primary_key=True)
    title = Column(String(100))
    author = Column(String(100))
    abstract  = Column(String(500))
    year = Column(Integer)
    venue = Column(String)

class Venue(Base):
    __tablename__="venue"
    name = Column(String(100),primary_key=True)
    abb = Column(String(20))
    publishing_house = Column(String(50))
    url = Column(String(200))
    big_rank = Column(String(5))
    small_rank = Column(Integer)


Base.metadata.create_all(engine)

if(__name__=="__main__"):
    total = session.query(Article).count()
    print(total)