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
    return a


def do_the_parse(DBLP_DATA_FILE,add_entity_func):

    start_from = 0
    try:
        with open('last_line.txt', 'r') as llf:
            start_from = int(llf.read())
            print("Re-start from [%d] " % start_from)
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
                entity = process_block_add_entity(block_content)
                add_entity_func(entity)
                block_content.clear()
            else:
                block_content.append(line)

