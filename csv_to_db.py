import csv
import sqlite3
import os
import sys

if len(sys.argv) <= 1:
    print('CSV formatted file is missing as argument.')
    exit()
    
cur_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(cur_dir, 'db', 'cards.db')
con = sqlite3.connect(db_path)
cur = con.cursor()

with open(os.path.join(cur_dir, sys.argv[1])) as fin:
    dr = csv.DictReader(fin, delimiter=';')
    to_db = [(1,i['question'],i['answer']) for i in dr]

tag = os.path.splitext(sys.argv[1])[0]
cur.execute('SELECT rowid from tag WHERE name=?', (tag,))
row = cur.fetchone()
if row == None:
    cur.execute("INSERT INTO tag (name) VALUES (?)", (tag,))
    rowid = cur.lastrowid
else:
    rowid = row[0]
cur.execute('SELECT max(rowid) FROM cards')
row = cur.fetchone()
if row == None:
    first_rowid = int(row[0]) + 1
else:
    first_rowid = 0

cur.executemany("INSERT INTO cards (type, front, back) VALUES (?, ?,REPLACE(?,'\\n','\n'))", to_db)
card_rowid = cur.lastrowid
cur.execute('SELECT rowid FROM cards WHERE rowid >= ? ORDER BY rowid ASC', (first_rowid,))
rows = cur.fetchall()
insert_list = []
for row in rows:
    insert_list.append((row[0], rowid,))

cur.executemany('INSERT INTO card_tag (card_id, tag_id) VALUES (?, ?)', insert_list)
con.commit()
con.close()
