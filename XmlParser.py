import csv
from xml.dom import minidom
import os
import subprocess
import datetime
import pandas as pd
class XmlParser:
   def __init__(self, parentTagName, elementList ,sourceFile):
      self.parentTagName = parentTagName
      self.elementList = elementList
      self.sourceFile = sourceFile
      	  
   def parseToList(self): 
      xmldoc = minidom.parse(self.sourceFile)
      itemlist = xmldoc.getElementsByTagName(self.parentTagName)
      print(len(itemlist))
      ItemListOp = []
      #colNames = ['link','title','description']
      for item in itemlist:
         articles = {}
         for colName in self.elementList:
            if item.getElementsByTagName(colName):
               articles[colName] = str(item.getElementsByTagName(colName)[0].firstChild.nodeValue).replace('\n','')
            else:
               articles[colName] = null
         articles['loaddate'] = str(datetime.datetime.utcnow())			   
         ItemListOp.append(articles)
      return ItemListOp
   def saveToCsv(self,itemList,targetFile):
       headers=['link','title','description','loaddate']
       with open(targetFile,'w') as f:
          writer= csv.DictWriter(f,fieldnames = headers,delimiter="|")
          writer.writeheader()
          writer.writerows(itemList)
#homePath = os.environ['APPHOME']
#out = subprocess.Popen(['ls', '/usr/src/app/Landing/'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#stdout,stderr = out.communicate()
#fileName=stdout.decode("utf-8").split("\n")[0]
#x1 = XmlParser('item',['link','title','description'],homePath + '/Landing/' + fileName )
#iList=x1.parseToList()
#targetF = homePath + '/parsedOutput.csv'
#x1.saveToCsv(iList,targetF)
#df = pd.DataFrame(iList)
#print(df.head())