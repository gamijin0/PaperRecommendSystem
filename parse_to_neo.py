import sys
import configparser
import os
from parse_raw_data import do_the_parse
from db_connection import add_entity_to_neo, add_entity_to_neo_only_relationship
sys.path.append("..")

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.cfg"))

DBLP_DATA_FILE = config.get("data", "dblp_data_file")
THREAD_NUM = int(config.get("other", "thread_num"))

if (__name__ == "__main__"):

    do_the_parse(
        DBLP_DATA_FILE=DBLP_DATA_FILE,
        add_entity_func=add_entity_to_neo,
        thread_num=THREAD_NUM,
    )
