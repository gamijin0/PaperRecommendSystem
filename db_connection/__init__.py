from .neo_orm import *
from .neo_connection import *

def __query_or_create(type_class, pri_key):

    new_one = type_class.select(dblp_graph,primary_value=pri_key).first()
    if(new_one is None):
        new_one = type_class()
    return new_one

def add_entity_to_neo(en):

    new_article = __query_or_create(Article,en.id)

    new_article.title = en.title
    new_article.article_id = en.id
    new_article.abstract = en.abstract
    new_article.year = en.year

    dblp_graph.push(new_article)

    venue = Venue()
    venue.name = en.venue
    new_article.published_in.add(venue)

    authors = en.author.split(',')
    for author_name in authors:
        a = __query_or_create(Author,author_name)
        a.name  = author_name
        new_article.authors.add(a)

    for ca_id in en.citation:
        ca = __query_or_create(Article,ca_id)
        ca.article_id = ca_id
        new_article.cite.add(ca)

    dblp_graph.push(new_article)


    print("[%s] has %d authors,cite %d other articles " % (str(en.id), len(authors), len(en.citation)))



def query_detail_by_id(id):
    a = Article.select(dblp_graph).where(article_id=id).first()
    return a

def query_id_by_word(word):
    articles =Article.select(dblp_graph).where("_.title =~ '.*%s.*' " % word)
    return [ a.article_id for a in list(articles)]

def query_article_id_by_year(year,limit):
    articles =Article.select(dblp_graph).where("_.year = %d " % year).limit(limit)
    return [ a.article_id for a in list(articles)]