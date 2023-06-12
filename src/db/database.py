import sqlite3
from sqlite3 import Error
from typing import Optional
import datetime


class Database:
    def __init__(self, db_file):
        """ initialize connection to the SQLite database """
        self.conn: Optional[sqlite3.Connection] = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.create_tables()
        except Error as e:
            print(e)

    def create_tables(self):
        """ create tables in the SQLite database"""
        sql_create_sold_number_records_table = """ CREATE TABLE IF NOT EXISTS sold_number_records (
                                                    id integer PRIMARY KEY,
                                                    link text NOT NULL,
                                                    number text NOT NULL,
                                                    status text NOT NULL,
                                                    price real NOT NULL,
                                                    sold_time text NOT NULL,
                                                    owner text
                                                ); """
        sql_create_sale_number_records_table = """ CREATE TABLE IF NOT EXISTS sale_number_records (
                                                    id integer PRIMARY KEY,
                                                    link text NOT NULL,
                                                    number text NOT NULL,
                                                    status text NOT NULL,
                                                    price real NOT NULL,
                                                    time_left text NOT NULL,
                                                    snapshot_time text NOT NULL,
                                                    owner text
                                                ); """
        if self.conn is not None:
            # create sold_number_records table
            self.create_table(sql_create_sold_number_records_table)
            # create sale_number_records table
            self.create_table(sql_create_sale_number_records_table)
        else:
            print("Error! cannot create the database connection.")

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_sold_number_record(self, record):
        """
        Insert a new SoldNumberRecord into the sold_number_records table,
        if the record does not exist. Return True if new record was inserted, False otherwise.
        """
        sql_check_exist = ''' SELECT 1 FROM sold_number_records WHERE link=? AND number=? AND status=? AND price=? AND sold_time=? AND owner=?'''
        cur = self.conn.cursor()
        cur.execute(sql_check_exist, record)
        if cur.fetchone():
            return False

        sql_insert = ''' INSERT INTO sold_number_records(link,number,status,price,sold_time, owner)
                VALUES(?,?,?,?,?,?) '''
        cur.execute(sql_insert, record)
        self.conn.commit()
        return True

    def insert_sale_number_record(self, record):
        """
        Insert a SaleNumberRecord into the sale_number_records table with a snapshot timestamp.
        """
        snapshot_time = datetime.datetime.now().isoformat()
        sql = ''' INSERT INTO sale_number_records(link,number,status,price,time_left, snapshot_time, owner)
                  VALUES(?,?,?,?,?,?,?) '''
        record_with_snapshot = record + (snapshot_time,)
        cur = self.conn.cursor()
        cur.execute(sql, record_with_snapshot)
        self.conn.commit()
        return cur.lastrowid
