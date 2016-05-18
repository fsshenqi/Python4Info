# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sqlite3

def database_init():
    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    cur.executescript('''
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track;

    CREATE TABLE Artist (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );

    CREATE TABLE Genre (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );

    CREATE TABLE Album (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        artist_id  INTEGER,
        title   TEXT UNIQUE
    );

    CREATE TABLE Track (
        id  INTEGER NOT NULL PRIMARY KEY
            AUTOINCREMENT UNIQUE,
        title TEXT  UNIQUE,
        album_id  INTEGER,
        genre_id  INTEGER,
        len INTEGER, rating INTEGER, count INTEGER
    );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def find_child(p, key):
    found = False
    for child in p:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None



all_artist_dict = {}
def artist_database_init(all):
    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    artist_dict = {}
    for dict in all:
        artist_name = find_child(dict, "Artist")
        if artist_name is None or artist_name == "": continue
        artist_dict[artist_name] = "1"
    for name in artist_dict.keys():
        cur.execute('''INSERT OR IGNORE INTO Artist (name)
            VALUES ( ? )''', (name,) )
    conn.commit()
    cur.execute('''SELECT name, id FROM Artist''')
    for item in cur:
        all_album_dict[item[0]] = item[1]
    conn.close()


all_album_dict = {}
def album_database_init(all):
    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    album_dict = {}
    for dict in all:
        artist_name = find_child(dict, "Artist")
        artist_id = get_artist_id_by_name(artist_name)
        album_name = find_child(dict, "Album")
        if album_name is None or album_name == "": continue
        album_dict[album_name] = artist_id
    for name, artist in album_dict.items():
        cur.execute('''INSERT OR IGNORE INTO Album (title,artist_id)
            VALUES ( ?,? )''', (name, artist))
    conn.commit()
    cur.execute('''SELECT title, id FROM Album''')
    for item in cur:
        all_album_dict[item[0]] = item[1]
    conn.close()


all_genre_dict = {}
def genre_database_init(all):
    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    genre_dict = {}
    for dict in all:
        genre = find_child(dict, "Genre")
        if genre is None or genre == "": continue
        genre_dict[genre] = "1"
    for name in genre_dict.keys():
        cur.execute('''INSERT OR IGNORE INTO Genre (name)
            VALUES ( ? )''', (name,) )
    conn.commit()
    cur.execute('''SELECT name, id FROM Genre''')
    for item in cur:
        all_genre_dict[item[0]] = item[1]
    conn.close()



def get_artist_id_by_name(name):
    id = None
    if name is None or name == "": return id
    id = all_artist_dict.get(name,None)
    if not id is None: return id

    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( name, ) )
    conn.commit()
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (name, ))
    try:
        id = cur.fetchone()[0]
    except:
        id = None

    cur.close()
    conn.close()

    return id


def get_album_id_by_name(name, artist_name):
    id = None
    if name is None or name == "": return id
    id = all_album_dict.get(name,None)
    if not id is None: return id

    artist_id = get_artist_id_by_name(artist_name)
    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    cur.execute('''INSERT OR IGNORE INTO Album (title,artist_id)
        VALUES ( ?,? )''', (name, artist_id) )
    conn.commit()
    cur.execute('SELECT id FROM Album WHERE title = ? ', (name, ))
    conn.commit()
    try:
        id = cur.fetchone()[0]
    except:
        id = None

    cur.close()
    conn.close()

    return id

def get_genre_id_by_name(name):
    id = None
    if name is None or name == "": return id
    id = all_genre_dict.get(name,None)
    if not id is None: return id

    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    cur.execute('''INSERT OR IGNORE INTO Genre (name)
        VALUES ( ? )''', (name,) )
    conn.commit()
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (name, ))
    try:
        id = cur.fetchone()[0]
    except:
        id = None
    cur.close()
    conn.close()
    return id


def track_database_init(all):
    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()

    for dict in all:
        track_id = find_child(dict, "Track ID")
        track = {}
        if track_id is None : continue
        track["title"] = find_child(dict, "Name")
        track["len"] = find_child(dict, "Total Time")
        track["rating"] = find_child(dict, "Rating")
        track["count"] = find_child(dict, "Play Count")
        artist_name = find_child(dict, "Artist")
        album_title = find_child(dict, "Album")
        genre_name = find_child(dict, "Genre")
        track["album_id"] = get_album_id_by_name(album_title, artist_name)
        track["genre_id"] = get_genre_id_by_name(genre_name)

        cur.execute('''INSERT OR IGNORE INTO Track (title, album_id, genre_id, len, rating, count)
            VALUES ( ?,?,?,?,?,? )''', ( track["title"], track["album_id"], track["genre_id"], track["len"], track["rating"], track["count"]) )
    conn.commit()
    cur.close()
    conn.close()


file_name = "Library.xml"
library = ET.parse(file_name)
all = library.findall('dict/dict/dict')
database_init()
artist_database_init(all)
album_database_init(all)
genre_database_init(all)
track_database_init(all)

def run():
    conn = sqlite3.connect("music.sqlite")
    cur = conn.cursor()
    cur.execute('''SELECT Track.title, Artist.name, Album.title, Genre.name
        FROM Track JOIN Genre JOIN Album JOIN Artist
        ON Track.genre_id = Genre.ID and Track.album_id = Album.id
            AND Album.artist_id = Artist.id
        ORDER BY Artist.name LIMIT 3''')
    for item in cur:
        print item
run()
