from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

class Article(GraphObject):
    __primarykey__ = "id"
    id = Property()
    title = Property()
    year = Property()
    abstract  = Property()
    authors = RelatedFrom("Author","publish")
    citers = RelatedFrom("Article","cite")
    published_in = RelatedTo("Venue")
    cite = RelatedTo("Article")

class Author(GraphObject):
    __primarykey__ = "name"
    name  = Property()
    published = RelatedTo("Article")


class Venue(GraphObject):
    __primarykey__ = "name"
    name = Property()
    articles = RelatedFrom("Article","published_in")


