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

    def cleanAll(self, tableName):
        inserSQL = "delete  from " + tableName

        try:  
            self.cursor.execute(inserSQL)
            self.db.commit()
        except:
            # Rollback in case there is any error
            print ("error :" + inserSQL )
            self.db.rollback()
    def cleanById(self, tableName, id):
        inserSQL = "delete  from {} where gameId = {}".format(tableName, id) 

        try:  
            self.cursor.execute(inserSQL)
            self.db.commit()
        except:
            # Rollback in case there is any error
            print ("error :" + inserSQL )
            self.db.rollback()

    def insert(self, data, tableName):
        inserSQL = "INSERT INTO "
        inserSQL += tableName
        inserSQL += " VALUES ("
        inserSQL += data 
        inserSQL += ")"

        try:  
            self.cursor.execute(inserSQL)
            self.db.commit()
        except:
            # Rollback in case there is any error
            # print ("error :" + data )
            self.db.rollback()


    def update(self, id, data, tableName):
        inserSQL = "UPDATE "
        inserSQL += tableName
        inserSQL += " SET "
        inserSQL += data 
        inserSQL += "where id = " + id

        try:  
            self.cursor.execute(inserSQL)
            self.db.commit()
        except:
            # Rollback in case there is any error
            print ("error :" + data )
            self.db.rollback()

    def updateId(self, main, time, tableName):
        inserSQL = "UPDATE "
        inserSQL += tableName
        inserSQL += " SET "
        inserSQL += "id = '" + str(main) + "_" + str(time) +"' "
        inserSQL += " where ((main = '" + str(main) + "') and ( time = " + str(time) + "))"

        try:  
            self.cursor.execute(inserSQL)
            self.db.commit()
        except:
            # Rollback in case there is any error
            print ("error :"  )
            self.db.rollback()

    def updateCommend(self, id, type,value, tableName):
        inserSQL = "UPDATE {} SET result = {} where ((id REGEXP '{}' )and(type = '{}'))".format(tableName, value, id, type)
        try:  
            self.cursor.execute(inserSQL)
            self.db.commit()
        except:
            # Rollback in case there is any error
            print ("error :"  )
            self.db.rollback()

    def queryByType(self, type, key):

        SQL = u"select * from {} where ( type = '{}' ) ".format(key, type)
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryByType  query error, sql:",SQL)
    
    def queryByTypeNum(self, type, key, num):

        SQL = u"select * from "+ key +" where ( type = '" + type + "' and num = '"+ num + "' ) "
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryByTypeNum  query error, sql:",SQL)

    def queryByTypeAll(self, key):

        SQL = u"select * from "+ key 
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryByTypeAll  query error, sql:",SQL)

    def queryById(self, key, id):
        SQL = u"select * from {} where (id REGEXP '{}')".format(key, id)  
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryById  query error, sql:",SQL)
    
    def queryCount(self, key, name):

        SQL = u"select count(*) from "+ key + " where (type = '" + name + "' ) "
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryCount  query error, sql:",SQL)
    
    def queryCountRate(self, type, key, result):

        SQL = u"select count(*) from "+ key +" where (( type = '" + type + "' ) and (rate_result = "+ result +")) "
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryCountRate  query error, sql:",SQL)
    
    def queryCountByID(self, key, id, type):
        SQL = u"select count(*) from {} where (id REGEXP '{}' and type = '{}') ".format(key, id, type)
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryCountByID  query error, sql:",SQL)
    
    def queryTeamDataMain(self, gameName, teamName, key):
        SQL = u"select * from "+ key +" where (( type like '%" + gameName + "%' ) and (main like '%"+ teamName +"%')) "
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryTeamDataMain  query error, sql:",SQL)
    
    def queryTeamDataClient(self, gameName, teamName, key):
        SQL = u"select * from "+ key +" where (( type like '%" + gameName + "%' ) and (client like '%"+ teamName +"%')) "
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryTeamDataClient  query error, sql:",SQL)
    
    def queryTeamData(self, gameName, teamName, key):
        SQL = u"select * from "+ key +" where (( type like '%" + gameName + "%' ) and ((main like '%"+ teamName +"%')) or (client like '%"+ teamName +"%'))"
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryTeamData  query error, sql:",SQL)
    
    def queryByTypeTime(self, gameName, key):
        SQL = u"select * from {} where ( type = '{}') order by time".format(key, gameName)
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("queryByTypeTime  query error, sql:",SQL)
    
    def updateMainFlag(self, gameName, value, key):
        SQL = "UPDATE {} SET flag = {} where (gameId = {})".format(key, value, gameName)
        SQL.encode('utf-8')

        try:  
            self.cursor.execute(SQL)
            results = self.cursor.fetchall()
            return results 
        except:
            print ("updateMainFlag  query error, sql:",SQL)

