from flask import Flask,request,jsonify,render_template
import pickle
import configparser
from db_session import session,Article
app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.cfg")
REVERSED_INDEX_FILE = config["data"]["reversed_index_file"]

reversedIndex = dict()

def myload():
    import os
    global reversedIndex
    if(os.path.exists(REVERSED_INDEX_FILE)):
        with open(REVERSED_INDEX_FILE,'rb') as f:
            reversedIndex = pickle.load(f)
            print("Load from [%s] successfully." % REVERSED_INDEX_FILE)
    else:
        print("Load Index file failed.")
        exit(0)

def get_details(id):
    res = session.query(Article).filter(Article.id==id).all()
    if(len(res)==0):
        return ""
    else:
        one = res[0]
        return one.title

@app.route('/query',methods=["GET","POST"])
def query_word_list():
    if(request.method == 'POST'):
        word_list  = [word.lower() for word in  request.form['word_list_str'].split(" ")]
        res = []
        for word in word_list:
            if(word in reversedIndex):
                if(len(res)==0):
                    res  = reversedIndex[word]
                else:
                    res  = res & reversedIndex[word]



        return jsonify(
            {"result":[
            {'id':id,"title":get_details(id)} for id in res
        ]}
        )
    else:
        return render_template("manual_query.html")

if __name__ == '__main__':
    myload()
    app.run(host="0.0.0.0",port=8080)