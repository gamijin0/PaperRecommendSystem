from .neo_orm import *
from .neo_connection import *



def add_entity_to_neo(en):
    new_article = Article()
    new_article.title = en.title
    new_article.id = en.id
    new_article.abstract = en.abstract
    new_article.year = en.year

    venue = Venue()
    venue.name = en.venue
    new_article.published_in.add(venue)

    authors = en.author.split(',')
    for author_name in authors:
        a = Author()
        a.name  = author_name
        new_article.authors.add(a)

    for ca_id in en.citation:
        ca = Article()
        ca.id = ca_id
        new_article.cite.add(ca)

    dblp_graph.push(new_article)


    print("[%s] has %d authors,cite %d other articles " % (str(en.id), len(authors), len(en.citation)))



def query_detail_by_id(id):
    a = Article.select(dblp_graph).where(id=id).first()



