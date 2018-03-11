import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "../config.cfg"))

n_username = config.get("neo4j", "username")
n_address = config.get("neo4j", "address")
n_port = config.get("neo4j", "port")
n_password = config.get("neo4j", "password")

from py2neo import Graph, Node, Relationship
dblp_graph = Graph(
    "%s:%s" % (n_address, n_port), username=n_username, password=n_password)
