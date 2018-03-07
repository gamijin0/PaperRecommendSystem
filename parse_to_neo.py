import sys
sys.path.append("..")

from db_connection import *
from parse_raw_data import do_the_parse

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.cfg"))

DBLP_DATA_FILE = config.get("data","dblp_data_file")

if(__name__=="__main__"):

    from db_connection import add_entity_to_neo
    do_the_parse(DBLP_DATA_FILE=DBLP_DATA_FILE,add_entity_func=add_entity_to_neo,thread_num=3)
