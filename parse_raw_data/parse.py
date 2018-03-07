import threading
import queue
import signal


BLOCK_QUEUE = queue.Queue(8)
STOP_WORK_FLAG = False

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


def worker(add_entity_func):
    while True:
        if(STOP_WORK_FLAG is True and BLOCK_QUEUE.empty()):
            break
        entity = BLOCK_QUEUE.get(block=True)
        add_entity_func(entity)
        BLOCK_QUEUE.task_done()

def feeder(DBLP_DATA_FILE):
    for entity in generate_entity_from_file(DBLP_DATA_FILE):
        if(STOP_WORK_FLAG):
            break
        BLOCK_QUEUE.put(entity,block=True)

def save_check_point(line_num):
    with open('last_line.txt', 'w') as outfile: outfile.write(str(line_num))

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
            a.id = int(line[6:])
        if (line[1] == "c"):
            a.venue = line[2:]
        if(line[1]=='!'):
            a.abstract=line[2:]
        if(line[1]=="%"):
            a.citation.add(int(line[2:]))
    return a

def generate_entity_from_file(DBLP_DATA_FILE):
    start_from = 0
    with open('last_line.txt', 'r') as llf:
        start_from = int(llf.read())
        print("Re-start from [%d] " % start_from)

    block_content = []

    with open(DBLP_DATA_FILE, 'r',encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i < start_from+1: continue
            if(len(line.strip())==0):
                entity = process_block_add_entity(block_content)
                block_content.clear()
                yield entity
                save_check_point(i)
            else:
                block_content.append(line)

def stop_work(signum=None, frame=None):
    global STOP_WORK_FLAG
    STOP_WORK_FLAG = True
    print("\n[Stopping now ...]\n")


signal.signal(signal.SIGINT,stop_work)
signal.signal(signal.SIGTERM,stop_work)


def do_the_parse(DBLP_DATA_FILE,add_entity_func,thread_num=2):

    worker_list = []

    for i in range(thread_num):
             t = threading.Thread(target=worker,args=(add_entity_func,))
             worker_list.append(t)
             t.start()

    feeder_thread = threading.Thread(target=feeder,args=(DBLP_DATA_FILE,))
    feeder_thread.start()

    print("Started %d workers and 1 feeder." % thread_num)

    while True:
        sig = input("\n================================================\n [  When you want to stop, please input 'stop'] \n================================================\n\n")
        if(sig=="stop"):
            stop_work()
            break
    BLOCK_QUEUE.join()
    exit()
