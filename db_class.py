from sqlalchemy import Column, TEXT, INT, BIGINT, BLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    user_id = Column(TEXT, nullable=False)
    password = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)
    preference = Column(TEXT, nullable=False)

    def __init__(self, user_id, password, email):
        # self.id = id
        self.user_id = user_id
        self.password = password
        self.email = email
        self.preference = 1


class MOVIE(Base):
    __tablename__ = 'movie_info'

    movie_index = Column(INT, primary_key=True)
    name = Column(TEXT)
    platform = Column(TEXT)
    director = Column(TEXT)
    casting = Column(TEXT)
    rating = Column(TEXT)
    original = Column(TEXT)
    year =  Column(TEXT)
    country = Column(TEXT)
    genre = Column(TEXT)
    running_time = Column(TEXT)
    age = Column(TEXT)
    description = Column(TEXT)
    
    def __init__(self, movie_index, name, platform, director, casting, rating, original, year, country, genre, running_time, age, description):

        self.movie_index = movie_index
        self.name = name
        self.platform = platform
        self.director = director
        self.casting = casting
        self.rating = rating
        self.original = original
        self.year = year
        self.country = country
        self.genre = genre
        self.running_time = running_time
        self.age = age
        self.description = description

class TV(Base):
    __tablename__ = 'tv_info'

    tv_index = Column(INT, primary_key=True)
    name = Column(TEXT)
    platform = Column(TEXT)
    director = Column(TEXT)
    casting = Column(TEXT)
    rating = Column(TEXT)
    original = Column(TEXT)
    year =  Column(TEXT)
    genre = Column(TEXT)
    country = Column(TEXT)
    age = Column(TEXT)
    description = Column(TEXT)
    channel = Column(TEXT)
    
    def __init__(self, tv_index, name, platform, director, casting, rating, original, year, genre, country, age, description, channel):

        self.tv_index = tv_index
        self.name = name
        self.platform = platform
        self.director = director
        self.casting = casting
        self.rating = rating
        self.original = original
        self.year = year
        self.country = country
        self.genre = genre
        self.age = age
        self.description = description
        self.channel = channel
    

class BOOK(Base):
    __tablename__ = 'book_info'

    book_index = Column(INT, primary_key=True)
    name = Column(TEXT)
    illustration = Column(TEXT)
    writer = Column(TEXT)
    rating = Column(TEXT)
    subtitle=Column(TEXT)
    author = Column(TEXT)
    category = Column(TEXT)
    year =  Column(TEXT)
    page = Column(TEXT)
    age = Column(TEXT)
    description = Column(TEXT)
    
    def __init__(self, book_index, illustration, writer, rating, subtitle, author, category, year, page, age, description):

        self.book_index = book_index
        self.illustration = illustration
        self.writer = writer
        self.rating = rating
        self.subtitle = subtitle
        self.author = author
        self.category = category
        self.year = year
        self.page = page
        self.age = age
        self.description = description
    
    