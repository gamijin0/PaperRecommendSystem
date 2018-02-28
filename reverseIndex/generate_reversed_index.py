# coding=utf-8
import logging
import re
import pickle
import sys
sys.path.append("..")
from db_session import Article as db_Article,session
import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__),"../config.cfg"))

Exception_log = config["log"]["exception_log"]

logging.basicConfig(filename=Exception_log, level=logging.ERROR)

REVERSED_INDEX_FILE = config["data"]["reversed_index_file"]
LAST_LINE_FILE = config['data']["last_line_file"]
DBLP_DATA_FILE = config['data']['dblp_data_file']


reversedIndex = dict()

def getWord(mystring):
    pat = '[a-zA-Z]+'
    res = re.findall(pat,mystring)
    for word in res:
        if(len(word)>=2):
            yield word.lower()

def addToHash(mystring,id):
    for word in getWord(mystring):
        if(word in reversedIndex):
            reversedIndex[word].add(id)
        else:
            new_set = set() #use set to avoid the repeat id
            new_set.add(id)
            reversedIndex[word] = new_set

class Article:
    id = ""
    title = ""
    author = ""
    year = ""
    journal = ""
    abstract = ""

    def addToReversedIndex(self):
        for property in [self.title,self.author,self.journal,self.abstract]:
            addToHash(property,self.id)


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
            a.journal = line[2:]
        if(line[1]=="!"):
            a.abstract = line[2:]

    # if(len(a.abstract)>0):
    #     session.query(db_Article).filter(db_Article.id==a.id).update({db_Article.abstract:a.abstract})
    #     session.commit()
    a.addToReversedIndex()

    print("[ %s ] added."%(a.id))


def mydump():

    with open(REVERSED_INDEX_FILE,'wb') as f:
        pickle.dump(obj=reversedIndex,file=f,protocol=2)
        print("Dump hash table to [%s]" % REVERSED_INDEX_FILE)

def myload():
    import os
    global reversedIndex
    if(os.path.exists(REVERSED_INDEX_FILE)):
        with open(REVERSED_INDEX_FILE,'rb') as f:
            reversedIndex = pickle.load(f)
            print("Load from [%s]" % REVERSED_INDEX_FILE)
    else:
        reversedIndex = dict()
        print("Generate a new HashTable.")


if(__name__=="__main__"):

    myload()

    start_from = 0
    try:
        with open(LAST_LINE_FILE, 'r') as llf:
            start_from = int(llf.read())
    except:
        pass

    block_content = []

    with open(DBLP_DATA_FILE, 'r',encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i < start_from+1: continue
            if(len(line.strip())==0):
                process_block_add_entity(block_content)
                block_content.clear()
                # if (i % 10000 == 0):
                #    with open(LAST_LINE_FILE, 'w') as outfile:
                #        outfile.write(str(i))
                #    mydump()
            else:
                block_content.append(line)

    mydump()
    print("Done.")
