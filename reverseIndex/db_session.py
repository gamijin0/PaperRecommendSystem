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
config.read("config.cfg")
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



Base.metadata.create_all(engine)

if(__name__=="__main__"):
    total = session.query(Article).count()
    print(total)