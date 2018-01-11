# coding: utf-8

# In[1]:

from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
import configparser
import random

config = configparser.ConfigParser()
config.read("../config.cfg")

m_username = config.get("mysql", "username")
m_address = config.get("mysql", "address")
m_port = config.get("mysql", "port")
m_password = config.get("mysql", "password")

n_username = config.get("neo4j", "username")
n_address = config.get("neo4j", "address")
n_port = config.get("neo4j", "port")
n_password = config.get("neo4j", "password")

dblp_graph = Graph(
    "%s:%s" % (n_address, n_port),
    username=n_username,
    password=n_password
)


class Article(GraphObject):
    __primarykey__ = 'title'
    title = Property()
    ee = Property()
    url = Property()
    key = Property()
    refer = RelatedTo("Article")
    be_refered_by = RelatedFrom("Article", "refer")
    pub_in = RelatedTo("journal", "published_in")


class journal(GraphObject):
    __primarykey__ = "name"
    name = Property()


# =========================================================

# coding=utf-8
import logging
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc
from sqlalchemy.sql.expression import func
import os
import time

logging.basicConfig(filename="exception.log", level=logging.ERROR)
# engine = create_engine("mysql+pymysql://%s:%s@%s:%s/DBLP" % (m_username, m_password, m_address, m_port), echo=False)
engine_local = create_engine("sqlite:///dblp.db", echo=False)
engine_remote = create_engine("mysql+pymysql://%s:%s@%s:%s/DBLP" % (m_username, m_password, m_address, m_port),
                              echo=False)

metadata = MetaData(engine_local)

Base = declarative_base()

from sqlalchemy.orm import sessionmaker

Session_local = sessionmaker()
Session_local.configure(bind=engine_local)
session_local = Session_local()

Session_remote = sessionmaker()
Session_remote.configure(bind=engine_remote)
session_remote = Session_remote()


class Reference_sql_local(Base):
    __tablename__ = "reference"
    article_id = Column(String(30), ForeignKey("article.id"), primary_key=True)
    citation_id = Column(String(30), ForeignKey("article.id"), primary_key=True)


class Article_sql_local(Base):
    __tablename__ = "article"
    id = Column(String(30), primary_key=True)
    title = Column(String(500))
    author = Column(String(100))
    year = Column(Integer)
    venue = Column(String)


class Article_sql_remote(Base):
    __tablename__ = "dblp"
    key = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    journal = Column(String)


def getSubString(title, bp=0.1, ep=0.9):
    title_len = len(a.title)
    begin = int(title_len * bp)
    end = int(title_len * ep)
    return title[begin:end]


if (__name__ == "__main__"):
    testSize = 100

    while (True):
        missed = 0
        articles = Article.select(dblp_graph).where("not exists(_.checked)").skip(random.randint(30000, 50000)).limit(
            testSize)
        for a in articles:
            query_res = session_local.query(Article_sql_local).filter(
                Article_sql_local.title.like("%" + getSubString(a.title, 0.1, 0.9) + "%")).all()
            # print("[%s]->[%d]" % (a.title,len(query_res)))
            if (len(query_res) == 0):
                missed += 1
        print("Miss percent: %f" % (missed / testSize))
        break

    refs = session_local.query(Reference_sql_local)

