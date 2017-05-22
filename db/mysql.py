#!/usr/bin/python
# coding=utf-8

import pymysql as MySQLdb 
import re
import sys


class sqlMgr:
    '''
    mysql 数据库管理模块
    '''


    def __init__(self, ipAddr, user, passwd, db_name):
        self.ipAddr = ipAddr
        self.user = user
        self.passwd = passwd
        self.db_name = db_name

        self.db = MySQLdb.connect(ipAddr, user, passwd, db_name, charset="utf8")
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def test(self):
        '''
        test function work
        '''       
        cursor = self.cursor
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print("Database version : %s " % data)

    def insert(self, data, tableName):
        inserSQL = "INSERT INTO "
        inserSQL += tableName
        inserSQL += " VALUES ("
        inserSQL += data 
        inserSQL += ")"
        # print(inserSQL)
        try:  
            self.cursor.execute(inserSQL)
            self.db.commit()
        except:
            # Rollback in case there is any error
            print ("error :" + data )
            self.db.rollback()

    def queryByType(self, type, key):

        SQL = u"select * from "+ key +" where ( type = '" + type + "' ) "
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("query error ")

    def queryByTypeAll(self, key):

        SQL = u"select * from "+ key 
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("query error ")
         