import pymysql as MySQLdb
import pandas as pd
import os
import csv
from pandas.io import sql
class Singleton:
  def __init__(self, klass):
    self.klass = klass
    self.instance = None
  def __call__(self, *args, **kwds):
    if self.instance == None:
      self.instance = self.klass(*args, **kwds)
    return self.instance

@Singleton
class Database:
  connection = None
  def getConnection(self):
    if self.connection is None:
      self.connection = MySQLdb.connect(host="arxiv-rss.cylz9khr50pz.us-east-2.rds.amazonaws.com", user="root", passwd="Amar123456", db="arxiv",local_infile=1)
    return self.connection
  def loadData(self,sql):
     if sql != '':
        cursor = self.connection.cursor()
        cursor.execute(sql)
        #data = cursor.fetchall()
        self.connection.commit()
        print ("Successfully Loaded :")
  def unloadData(self,sql):
     df = pd.read_sql(sql,self.connection)
     return df
  def unloadToCsv(self,df,unloadFile):
     print(unloadFile)
     df.to_csv(unloadFile, encoding='utf-8', header = True, doublequote = False, sep='|', index=False,quoting = csv.QUOTE_NONE, escapechar = ' ')
  def closeConnection(self):
     self.connection.close()
  def dfToMysql(self,df,tableName):
     df.to_sql(con=self.connection, name=tableName, if_exists='append', flavor='mysql')

#homePath = os.environ['APPHOME']
#Database().getConnection()
#targetS = homePath + '/a.csv'
#targetF = homePath + '/unload.csv'
#load_sql = "LOAD DATA LOCAL INFILE '/usr/src/app/parsedOutput.csv' INTO TABLE tasks FIELDS TERMINATED BY '|' IGNORE 1 LINES (link,title,description,loaddate);"
#Database().loadData('USE arxiv')
#Database().loadData(load_sql)
#sqlI='select link,title,description from tasks'
#df1 = Database().unloadData(sqlI)
#print(df1.head(2))
#Database().closeConnection()
