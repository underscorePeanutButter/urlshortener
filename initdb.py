import sqlite3

db = sqlite3.connect("urls.db")

command = """
CREATE TABLE Urls (
shortened_tag VARCHAR,
full_url VARCHAR,
creation_time BIGINT)"""
db.execute(command)

db.commit()