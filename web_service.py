from flask import Flask, request, jsonify, render_template, send_file
import pickle
import configparser
import os

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.cfg"))
REVERSED_INDEX_FILE = config["data"]["reversed_index_file"]
WORDCLOUD_DIR = config["data"]['wordcloud_dir']
reversedIndex = dict()

USE_ReverseIndex = False


def myload():
    import os
    global reversedIndex
    if (os.path.exists(REVERSED_INDEX_FILE)):
        with open(REVERSED_INDEX_FILE, 'rb') as f:
            reversedIndex = pickle.load(f)
            print("Load from [%s] successfully." % REVERSED_INDEX_FILE)
    else:
        print("Load Index file failed.")
        exit(0)


def get_details(id):
    from db_connection import query_detail_by_id
    one = query_detail_by_id(id)
    if (not one):
        return ""
    else:
        return {'title': one.title, "abstract": one.abstract, 'venue': str(list(one.published_in)), 'author': str(list(one.authors))}


def query_ids_by_words_from_reverse_index(word_list):
    res = set()
    for word in word_list:
        if (word in reversedIndex):
            if (len(res) == 0):
                res = set(reversedIndex[word])
            else:
                res = res & set(reversedIndex[word])
    return res





def query_ids_by_words_from_databases(word_list):
    from db_connection import query_id_by_word
    res = set()
    for word in word_list:
        if (len(res) == 0):
            res = set(query_id_by_word(word))
        else:
            res = res & set(query_id_by_word(word))
    return res


def get_word_list_from_request(request):
    word_list = [word.lower() for word in request.form['word_list_str'].split(" ")]
    return word_list


def get_content_by_year(year):

    from db_connection import query_article_id_by_year
    ids = query_article_id_by_year(year,500)

    content = ""
    for id in ids:
        en = get_details(id)
        content+=" "+en['title']
        content+=" "+en["abstract"]
    return content


@app.route('/wordcloud', methods=["POST"])
def word_cloud_sample():

    from wordcloud import WordCloud,STOPWORDS
    mySTOPWORDS = ["paper","process","application","project","present","practice","results","models","work","component","used","however","use","new","also","time","user","based","system","model","using","data","problem","approach","technique","result","method","information"]+list(STOPWORDS)
    import time
    import os
    if (not os.path.isdir(WORDCLOUD_DIR)):
        os.mkdir(WORDCLOUD_DIR)
    year = int(request.form['year'])
    content = get_content_by_year(year=year)
    wordcloud = WordCloud(background_color="white", width=1000, height=860, stopwords=mySTOPWORDS, margin=2).generate(content.lower())
    wc_name = str(time.time())[:10] + ".png"
    wordcloud.to_file(os.path.join(WORDCLOUD_DIR, wc_name))
    return send_file(os.path.join(WORDCLOUD_DIR, wc_name), mimetype='image/gif')


def get_article_id_by_words(word_list):
    if (USE_ReverseIndex):
        ids = query_ids_by_words_from_reverse_index(word_list=word_list)
    else:
        ids = query_ids_by_words_from_databases(word_list=word_list)
    return ids





@app.route('/query', methods=["GET", "POST"])
def query_word_list():
    if (request.method == 'POST'):
        word_list = get_word_list_from_request(request=request)
        ids = get_article_id_by_words(word_list=word_list)
        return jsonify(
            {"result": [
                {'id': id, "details": get_details(id)} for id in ids
            ]}
        )
    else:
        return render_template("manual_query.html")


@app.route('/authors', methods=["POST"])
def query_authors_by_words():
    word_list = get_word_list_from_request(request=request)
    ids = query_ids_by_words_from_reverse_index(word_list=word_list)
    return jsonify(
        {"result": [
            {'id': id, "authors": get_details(id)} for id in ids
        ]}
    )


if __name__ == '__main__':
    import sys

    if (len(sys.argv) == 2 and sys.argv[1] == "r"):
        USE_ReverseIndex = True
        myload()
    print("Ready.")
    app.run(host="0.0.0.0", port=8080)
