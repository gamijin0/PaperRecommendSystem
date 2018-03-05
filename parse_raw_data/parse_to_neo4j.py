# coding=utf-8
"""
解析数据库中的xml格式
"""
import logging
from py2neo import Graph, Node, Relationship
import os
import time
import configparser

logging.basicConfig(filename="exception.log", level=logging.ERROR)
# engine = create_engine("mysql+pymysql://%s:%s@%s:%s/DBLP" % (m_username, m_password, m_address, m_port), echo=False)
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.cfg"))

n_username = config.get("neo4j", "username")
n_address = config.get("neo4j", "address")
n_port = config.get("neo4j", "port")
n_password = config.get("neo4j", "password")

DBLP_DATA_FILE = config.get("data","dblp_data_file")

from py2neo import Graph, Node, Relationship
graph = Graph(
    "%s:%s" % (n_address, n_port),
    username=n_username,
    password=n_password
)

from py2neo import Graph, Node, Relationship

dblp_graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="19961020"
)

#添加实体，并对关系进行处理
def addEntity(en):
    print(len(en.citation))
    if (en.author == None):
        return

#定义三种类型节点
    article = Node("Article", title=en.title,id=en.id,abstract=en.abstract,year=en.year)
    author = Node("Author", id=en.author)
    venue = Node("Venue", id=en.venue)

#定义关系       （可能需要加入作者间的合作关系：考虑双向关系，可以查询时完全不考虑方向）
    publish = Relationship(author, "publish", article)
    published_in = Relationship(article, "published_in", venue)

#合并插入节点及关系
    dblp_graph.merge(article)
    dblp_graph.merge(author)
    dblp_graph.merge(venue)
    dblp_graph.merge(publish)
    dblp_graph.merge(published_in)
    #将所有的引用放入列表内，当节点在列表中创建关系，最后合并节点
    for i in en.citation:
        article2= Node("Article",id=i)
        cite=Relationship(article,"cite",article2)
        dblp_graph.merge(article2)
        dblp_graph.merge(cite)
        #print("[%s]-->[%s]" % (str(en.id),str(i)))


#定义article的节点类
class Article():
    id = 0
    title = ""
    author = ""
    year = ""
    venue = ""
    abstract= ""
    citation=set()
    def __init__(self):
        self.id=0
        self.citation = set()
        self.title = ""
        self.author = ""
        self.year = ""
        self.venue = ""
        self.abstract = ""

#将一个论文内的所有属性放入一个block内，进行匹配提取
def process_block_add_entity(block_content):
    """
    example:
        #*Applying the genetic encoded conceptual graph to grouping learning.
        #@Teyi Chan,Chien-Ming Chen,Yu-Lung Wu,Bin-Shyan Jong,Yen-Teh Hsia,Tsong-Wuu Lin
        #t2010
        #cExpert Syst. Appl.
        #index1594522
        #%1285396
        #%928856
        #%1112994
        #%890842
        #!The continual
    """
    a = Article()
    for l in block_content:
        line = l.strip()
        if (line[1] == "*"):
            a.title = line[2:]
        if (line[1] == "@"):
            a.author = line[2:]
        if (line[1] == "t"):
            a.year = int(line[2:])
        if (line[1] == "i"):
            a.id = line[6:]
        if (line[1] == "c"):
            a.venue = line[2:]
        if(line[1]=='!'):
            a.abstract=line[2:]
        if(line[1]=="%"):
            a.citation.add(int(line[2:]))
    addEntity(a)
    print("[ %s ] added."%(a.id))



if(__name__=="__main__"):
    start_from = 0
    try:
        with open('last_line.txt', 'r') as llf:
            start_from = int(llf.read())
    except:
        pass

    block_content = []

    with open(DBLP_DATA_FILE, 'r',encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i < start_from+1: continue
            if(len(line.strip())==0):
                # print("spcae [%d]" % (i))
                # time.sleep(0.1)
                with open('last_line.txt', 'w') as outfile: outfile.write(str(i))
                process_block_add_entity(block_content)
                block_content.clear()
            else:
                block_content.append(line)





