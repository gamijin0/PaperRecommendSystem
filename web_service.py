from flask import Flask, request, jsonify, render_template,send_file
import pickle
import configparser
import os

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.cfg"))
REVERSED_INDEX_FILE = config["data"]["reversed_index_file"]
WORDCLOUD_DIR  = config["data"]['wordcloud_dir']
reversedIndex = dict()


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
        return {'title': one.title, "abstract": one.abstract, 'venue': one.venue, 'author': one.author}


def query_ids_by_words_from_reverse_index(word_list):
    res = []
    for word in word_list:
        if (word in reversedIndex):
            if (len(res) == 0):
                res = reversedIndex[word]
            else:
                res = res & reversedIndex[word]
    return res


def get_word_list_from_request(request):
    word_list = [word.lower() for word in request.form['word_list_str'].split(" ")]
    return word_list


def get_content_from_title_by_ids(ids):
    return [ get_details(id)['title'] for id in ids ]

@app.route('/wordcloud', methods=["POST"])
def word_cloud_sample():
    from wordcloud import WordCloud
    import time
    import os
    if (not os.path.isdir(WORDCLOUD_DIR)):
        os.mkdir(WORDCLOUD_DIR)
    word_list = get_word_list_from_request(request=request)
    ids = query_ids_by_words_from_reverse_index(word_list=word_list)
    content = get_content_from_title_by_ids(ids=ids)
    wordcloud = WordCloud(background_color="white", width=1000, height=860, margin=2).generate(" ".join(content))
    wc_name = str(time.time())[:10]+".png"
    wordcloud.to_file(os.path.join(WORDCLOUD_DIR,wc_name))
    return send_file(os.path.join(WORDCLOUD_DIR,wc_name), mimetype='image/gif')

@app.route('/query', methods=["GET", "POST"])
def query_word_list():
    if (request.method == 'POST'):
        word_list = get_word_list_from_request(request=request)
        ids = query_ids_by_words_from_reverse_index(word_list=word_list)
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
    myload()
    app.run(host="0.0.0.0", port=8080)
