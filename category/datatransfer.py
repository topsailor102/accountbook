import sqlite3
import csv
import os

db_name = "db.sqlite3"

def get_date_from_the_file(csvfile):
    print("csvfile: {}, {}".format(csvfile, csvfile.split('.')[-1]))
    if csvfile.split('.')[-1] != 'csv':
        print("file type is not expected format.")
    else:
        print("it's csv file!")
        
        query_set = ""
        with open (csvfile, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dateinfo = row['DATEINFO']
                place = row['PLACE']
                cost = row['COST']
                summary = row['SUMMARY']
                isfixed = row['ISFIXED']
                creationinfo = row['CREATIONINFO']
                sector_id = row['SECTOR']
                way_id = row['WAY']
                insert_query = f'INSERT INTO category_expense (\'DATEINFO\', \'PLACE\', \'COST\', \'SUMMARY\',\
                                 \'ISFIXED\', \'CREATIONINFO\', \'SECTOR_ID\', \'WAY_ID\') \
                                 VALUES (\'{dateinfo}\', \'{place}\', {cost}, \'{summary}\', \
                                         {isfixed}, \'{creationinfo}\', {sector_id}, {way_id});\n'

                query_set += insert_query
        #print(query_set)
        insert_data_to_db(query_set, db_name)
        return query_set

def insert_data_to_db(query, db_name):
    con = sqlite3.connect(db_name)
    c = con.cursor()
    
    #for line in con.iterdump():
    #    print(line)
    #query = f'DELETE from category_expense WHERE DATEINFO < "2020-04-26";'
    c.executescript(query)
        
    c.close()
    con.close()    