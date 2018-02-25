# coding=utf-8
import logging
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
import os
import time

from ..db_session import session,Base,engine


class Reference(Base):
    __tablename__="reference"
    article_id = Column(String(30),ForeignKey("article.id"),primary_key=True)
    citation_id = Column(String(30),ForeignKey("article.id"),primary_key=True)


class Article(Base):
    __tablename__="article"
    id = Column(String(30),primary_key=True)
    title = Column(String(500))
    author = Column(String(100))
    year = Column(Integer)
    venue = Column(String)



Base.metadata.create_all(engine)


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
    session.add(a)
    session.commit()
    print("[ %s ] added."%(a.id))


def process_block_add_reference(block_content):
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
    for l in block_content:
        line = l.strip()
        if (line[1] == "i"):
            id = line[6:]
        if(line[1]=="%"):
            citation = Reference()
            citation.article_id = id
            citation.citation_id = line[2:]
            session.add(citation)
            session.commit()
            print("[ %s ] ->[ %s ]" % (citation.article_id,citation.citation_id))




if(__name__=="__main__"):

    start_from = 0
    try:
        with open('last_line.txt', 'r') as llf:
            start_from = int(llf.read())
    except:
        pass

    block_content = []

    with open('D:\\Data\\PRS_DATA\\DBLPOnlyCitationOct19.txt', 'r',encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i < start_from+1: continue
            if(len(line.strip())==0):
                # print("spcae [%d]" % (i))
                # time.sleep(0.1)
                with open('last_line.txt', 'w') as outfile: outfile.write(str(i))
                process_block_add_reference(block_content)
                block_content.clear()
            else:
                block_content.append(line)


