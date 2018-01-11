# coding: utf-8

# In[1]:

from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
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
    be_refered_by = RelatedFrom("Article", "refer")
    pub_in = RelatedTo("journal", "published_in")


class journal(GraphObject):
    __primarykey__ = "name"
    name = Property()


# In[2]:

articles = Article.select(dblp_graph).limit(3)
for a in articles:
    print(a.title)

# In[3]:

import socket
import socks
import requests

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket
import scholarly

for a in articles:
    pubs = scholarly.search_pubs_query(a.title)
    p = next(pubs)

    citations = list(p.get_citedby())

    s = "//" + "=" * 10 + "[%d] cited " + p.bib['title'] + "=" * 10 % (len(citations))
    print(s)

    for citation in citations:
        res = Article.select(dblp_graph).where('_.title =~ "(?i).*%s.*"' % (citation.bib['title']))
        if (len(list(res)) != 0):
            print(citation.bib['title'])
    print("=" * len(s))

