import csv
import sqlite3
import os
import sys

if len(sys.argv) <= 1:
    print('CSV formatted file is missing as argument.')
    exit()
    
cur_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(cur_dir, 'toremove', 'cards.db')
con = sqlite3.connect(db_path)
cur = con.cursor()

with open(os.path.join(cur_dir, 'csv_flashcards', sys.argv[1])) as fin:
    dr = csv.DictReader(fin, delimiter=';')
    to_db = [(1,i['question'],i['answer']) for i in dr]

cur.executemany('INSERT INTO cards (type, front, back) VALUES (?, ?, ?)', to_db)
con.commit()
con.close()
