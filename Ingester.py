import requests
class Ingester:
   def __init__(self, type , sourceUrl, targetFileName):
      self.type = type
      self.sourceUrl = sourceUrl
      self.targetFileName = targetFileName
   def ingestRssFeed(self):
      resp = requests.get(self.sourceUrl)
      with open(self.targetFileName,'wb') as f:
        f.write(resp.content)