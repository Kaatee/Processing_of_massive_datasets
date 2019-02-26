import sqlite3
import datetime

db = sqlite3.connect('test.db')
cursor = db.cursor()

start = datetime.datetime.now()

cursor.execute("DROP INDEX IF EXISTS index_name")
cursor.execute("DROP INDEX IF EXISTS index_name2")
cursor.execute("DROP INDEX IF EXISTS index_name3")
cursor.execute("DROP TABLE IF EXISTS tracks;")
cursor.execute("DROP TABLE IF EXISTS samples;")
cursor.execute("DROP TABLE IF EXISTS dates;")
cursor.execute("CREATE TABLE tracks (track_id VARCHAR(18) NOT NULL, song_id VARCHAR(18) NOT NULL, artist VARCHAR(256) DEFAULT NULL,title VARCHAR(256) DEFAULT NULL,PRIMARY KEY (track_id))")
cursor.execute("CREATE TABLE dates (id INTEGER PRIMARY KEY AUTOINCREMENT , day INTEGER, month INTEGER, year INTEGER )")
cursor.execute("CREATE TABLE samples ( user_id VARCHAR(40) NOT NULL, song_id VARCHAR(18) NOT NULL, date_id INTEGER, FOREIGN KEY(date_id) REFERENCES dates(id) )")
cursor.execute("CREATE UNIQUE INDEX index_name ON tracks (song_id);")

db.commit()

#download data from unique_tracks.txt
with open("unique_tracks.txt", encoding='iso-8859-2', errors='replace') as file:
    for line in file:
        row = line.replace("\n","").split("<SEP>")
        cursor.execute('INSERT OR REPLACE INTO tracks (track_id, song_id, artist , title) VALUES (?, ?, ?,?)', (row[0], row[1], row[2], row[3]))

#download data from triplets_sample_20p.txt
with open("triplets_sample_20p.txt", encoding='iso-8859-2', errors='replace') as file:
    for line in file:
        row = line.split("<SEP>")
        datee = datetime.datetime.fromtimestamp(int(row[2]))
        cursor.execute('INSERT INTO dates (day, month, year) VALUES (?,?,?)',(datee.strftime("%d"), datee.strftime("%m"), datee.strftime("%y")))
        date_id = cursor.lastrowid
        cursor.execute('INSERT INTO samples (user_id, song_id, date_id) VALUES (?, ?, ?)', (row[0], row[1], date_id))

db.commit()
cursor.execute("CREATE INDEX index_name2 ON samples (song_id)")
cursor.execute("CREATE INDEX index_name3 ON tracks (artist)")
db.commit()

# ----   QUERY 1 ------
cursor.execute("SELECT tracks.title, tracks.artist, sub.counter FROM ( SELECT song_id, COUNT(song_id) AS counter FROM samples GROUP BY song_id ORDER BY counter DESC LIMIT 10) sub INNER JOIN tracks ON (tracks.song_id = sub.song_id) ORDER BY sub.counter DESC;")
for x in cursor.fetchall():
    print(' '.join([str(i) for i in x]))


# ----   QUERY 2 ------
cursor.execute("SELECT user_id, COUNT(DISTINCT song_id) AS counter FROM samples GROUP BY user_id ORDER BY counter DESC LIMIT 10;")
for x in cursor.fetchall():
    print(' '.join([str(i) for i in x]))


# ----   QUERY 3 ------
cursor.execute("SELECT artist, SUM(suma) AS counter FROM (SELECT tracks.artist, t.song_id, t.suma  FROM (SELECT song_id, COUNT(song_id) AS suma FROM samples GROUP BY song_id) t JOIN tracks ON (t.song_id = tracks.song_id)) GROUP BY artist ORDER BY counter DESC LIMIT 1;")
for x in cursor.fetchall():
    print(' '.join([str(i) for i in x]))


# ----   QUERY 4 ------
cursor.execute("SELECT month, COUNT(song_id) FROM  samples JOIN dates ON (samples.date_id = dates.id) GROUP BY month ORDER BY month;")
for x in cursor.fetchall():
    print(' '.join([str(i) for i in x]))


# ----   QUERY 5 ------
cursor.execute("SELECT samples.user_id FROM samples WHERE song_id IN (SELECT samples.song_id FROM samples JOIN tracks WHERE samples.song_id = tracks.song_id AND tracks.artist LIKE 'Queen' GROUP BY samples.song_id ORDER BY COUNT(samples.song_id) DESC LIMIT 3) GROUP BY user_id HAVING COUNT(DISTINCT samples.song_id) >= 3 ORDER BY user_id LIMIT 10")
for x in cursor.fetchall():
    print(' '.join([str(i) for i in x]))

db.close()