
# coding: utf-8

# In[15]:

from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject,Property,RelatedTo,RelatedFrom
import configparser


config = configparser.ConfigParser()
config.read("config.cfg")

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
    be_refered_by = RelatedFrom("Article","refer")
    pub_in = RelatedTo("journal","published_in")
class journal(GraphObject):
    __primarykey__ = "name"
    name = Property()


# In[16]:

articles = Article.select(dblp_graph).limit(10)


# In[18]:

for a in articles:
    for j in a.pub_in:
        if(a.refer):
            print(a.ee)

