import sqlite3

def create_music_db():
	conn = sqlite3.connect('music.sqlite3')
	cur = conn.cursor()
	cur.execute('DROP TABLE IF EXISTS Tracks ')
	cur.execute('CREATE TABLE Tracks (title TEXT, plays INTEGER)')
	conn.close()

def show_musics():
	conn = sqlite3.connect('music.sqlite3')
	cur = conn.cursor()
	cur.execute('SELECT * FROM Tracks')
	print "music:"
	for music in cur:
		print music
	conn.close()

def insert_music():
	conn = sqlite3.connect('music.sqlite3')
	cur = conn.cursor()
	cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)', ('My May', 15))
	cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)', ('Thunder struck', 20))
	conn.commit()
	conn.close()

def clear_music():
	conn = sqlite3.connect('music.sqlite3')
	cur = conn.cursor()
	cur.execute('DELETE FROM Tracks ')
	conn.commit()
	cur.close()

create_music_db()
insert_music()
show_musics()
clear_music()
show_musics()
