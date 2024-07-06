import requests
import json
import os
from dotenv import load_dotenv
from endpoints import api_url, api_urlelo, api_urlsummid, api_urlnamecheck

class LeagueAcc():
     def __init__(self, loginname,pw, summoner, tagline):
          self.loginname = loginname
          self.summoner = summoner
          self.pw = pw
          self.tagline = tagline
          self.elo = None
          self.id = None
          self.puuid = None
          load_dotenv()
          

     def setPuuid(self, puuid):
         self.puuid = puuid
     def setid(self, id):
         self.id = id

     def setEloUnranked(self):
        self.elo = 'UNRANKED'
     def setElo(self, elo):
        self.elo = elo
     


     def reloadElo(self):
         playerdata = requests.get(api_urlelo + self.id +'?api_key=' + os.getenv('apikey'))
         data2 = playerdata.json()       
         for data in data2:
            if data['queueType'] == 'RANKED_SOLO_5x5':
                self.elo = data['tier']+' '+data['rank']+' '+str(data['leaguePoints'])
              
     
     
     def reloadName(self):
          try:
            result = requests.get(api_urlnamecheck + self.puuid +'?api_key=' + os.getenv('apikey'))
            self.tagline = result.json()['tagLine']
            self.summoner = result.json()['gameName']
          except:
            return False
     
     def loadData(self):
         
         try:
            result = requests.get(api_url+ self.summoner +'%20/'+ self.tagline + '?api_key=' +os.getenv('apikey'))
            self.puuid = result.json()['puuid']
            
            summid = requests.get(api_urlsummid + self.puuid +'?api_key=' + os.getenv('apikey'))
            self.id = summid.json()['id']
            self.reloadElo()
            if self.elo == None:
                self.setEloUnranked()
            return True
         except:
            return False
           
        
     def from_json(json_dct):
      return LeagueAcc(
          json_dct['elo'],
          json_dct['id'],
          json_dct['loginname'],
          json_dct['puuid'],
          json_dct['pw'],
          json_dct['summoner'],
          json_dct['tagline'])
     

     def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=7)
