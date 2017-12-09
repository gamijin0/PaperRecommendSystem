# coding: utf-8

# In[8]:
import logging
import configparser
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

config = configparser.ConfigParser()
config.read("config.cfg")

m_username = config.get("mysql", "username")
m_address = config.get("mysql", "address")
m_port = config.get("mysql", "port")
m_password = config.get("mysql", "password")

n_username = config.get("neo4j", "username")
n_address = config.get("neo4j", "address")
n_port = config.get("neo4j", "port")
n_password = config.get("neo4j", "password")

logging.basicConfig(filename="exception.log", level=logging.ERROR)
engine = create_engine("mysql+pymysql://%s:%s@%s:%s/DBLP" % (m_username, m_password, m_address, m_port), echo=False)
# engine=create_engine("sqlite:///dblp.db",echo=True)

Base = declarative_base()
metadata = MetaData(engine)

# In[9]:

Dblp_class = Table("dblp", metadata, autoload=True)

# In[10]:

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# In[11]:

total_num = session.query(Dblp_class).count()
print(total_num)

# In[12]:

from py2neo import Graph, Node, Relationship

dblp_graph = Graph(
    "%s:%s" % (n_address, n_port),
    username=n_username,
    password=n_password
)


def add_entity(en):
    if not en.author:
        return

    article = Node("Article", title=en.title, url=en.url, ee=en.ee, key=en.key)
    author = Node("author", name=en.author)
    journal = Node("journal", name=en.journal)

    modify = Relationship(author, "modify", article)
    modify['mdate'] = str(en.mdate)
    published_in = Relationship(article, "published_in", journal)
    published_in['year'] = en.year
    published_in['pages'] = en.pages
    published_in['volume'] = en.volume

    dblp_graph.merge(article)
    dblp_graph.merge(author)
    dblp_graph.merge(journal)
    dblp_graph.merge(modify)
    dblp_graph.merge(published_in)

    print("Add:[ %s ]" % en.title[:20])


# In[13]:

TRANSFORMED_TAG = 2

while (True):
    some_entity = session.query(Dblp_class).filter(Dblp_class.columns.transformed != TRANSFORMED_TAG).limit(1).all()
    if (len(some_entity) == 0):
        logging.error("Done.")
        break
    for i, en in enumerate(some_entity):
        try:
            add_entity(en)
            session.execute("update dblp set transformed=%d WHERE dblp.key = '%s';" % (TRANSFORMED_TAG, en.key))
            session.commit()
        except Exception as e:
            print(e)
            logging.error(str(e))

            # match (j:journal),((a:Article)-[:published_in]->(j)),((h:author)-[:modify]->(a)) return collect(a)[..20] as A,collect(h)[..20] as H,j
            # match (author:author)-[m]->(article)-[p]->(journal:journal)
            # with author,count(distinct journal) as cnt
            # where cnt > 1
            # return * limit 20
