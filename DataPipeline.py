from Ingester import Ingester
from XmlParser import XmlParser
from connectMySql import Database
import pandas as pd
import datetime
import os
homePath = os.environ['APPHOME']
tz = str(datetime.datetime.utcnow())

# Ingesting
print("Ingesting RSS feed")
I = Ingester('RSS','http://export.arxiv.org/rss/cs', homePath + '/Landing/cs_'+ tz +'.xml')
I.ingestRssFeed()

# XmlParsing
print("Parsing XML to DataFrame")
#out = subprocess.Popen(['ls', '/usr/src/app/Landing/'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#stdout,stderr = out.communicate()
#fileName=stdout.decode("utf-8").split("\n")[0]
x1 = XmlParser('item',['link','title','description'],homePath + '/Landing/cs_'+ tz +'.xml')
iList=x1.parseToList()
targetF = homePath + '/parsedOutput.csv'
x1.saveToCsv(iList,targetF)
df1 = pd.DataFrame(iList)

print("Unloading Target Data")
# Load to Db

Database().getConnection()
targetF = homePath + '/unload.csv'
load_sql = "LOAD DATA LOCAL INFILE '/usr/src/app/parsedOutput.csv' INTO TABLE tasks FIELDS TERMINATED BY '|' IGNORE 1 LINES (link,title,description,loaddate);"
#Database().loadData('USE arxiv')
#Database().loadData(load_sql)
sqlI='select link,title,description from tasks'
df2 = Database().unloadData(sqlI)
df2['targetLink'] = df2['link']


targetDf = pd.merge(df1,df2,how='left',on=['link'])

filtered_df = targetDf[targetDf['targetLink'].isnull()]
op = filtered_df[['link','title_x','description_x','loaddate']]

targetF = homePath + '/parsedOutput.csv'

Database().unloadToCsv(op,targetF)

load_sql = "LOAD DATA LOCAL INFILE '/usr/src/app/parsedOutput.csv' INTO TABLE tasks FIELDS TERMINATED BY '|' IGNORE 1 LINES (link,title,description,loaddate);"
Database().loadData('USE arxiv')
Database().loadData(load_sql)
Database().closeConnection()