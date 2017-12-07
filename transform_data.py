# coding: utf-8

# In[8]:
import logging

logging.basicConfig(filename="exception.log", level=logging.DEBUG)

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:xlsd1996@chaos.ac.cn:3306/DBLP", echo=True)
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
    "http://chaos.ac.cn:7474",
    username="neo4j",
    password="xlsd1996"
)


def addEntity(en):
    print("Add:[ %s ]" % en.title[:20])
    article = Node("Article", title=en.title)
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


# In[13]:

while (True):
    some_entity = session.query(Dblp_class).filter(Dblp_class.columns.transformed == 0).limit(20).all()
    if (len(some_entity) == 0):
        logging.debug("Done")
        break
    for i, en in enumerate(some_entity):
        try:
            addEntity(en)
            session.execute("update dblp set transformed=1 WHERE dblp.key = '%s';" % (en.key))
            session.commit()
        except Exception() as e:

            logging.debug(str(e))

# match (j:journal),((a:Article)-[:published_in]->(j)),((h:author)-[:modify]->(a)) return collect(a)[..20] as A,collect(h)[..20] as H,j
