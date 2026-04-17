import pandas as pd
from datetime import datetime
from src.utils.customException import handle_exceptions
from src.utils.customLogger import logger
from pathlib import Path

@handle_exceptions
def readData(datapath:str):

   # Function to read any .xlsx file as DataFrame

   logger.info(f"{Path(__file__).name}: reading {datapath} as DataFrame")

   df = pd.read_excel(datapath)
   return df

import yaml
from types import SimpleNamespace

@handle_exceptions
def loadConfig(config):
  
  # Function to read yaml

   with open(config, "r") as f:
      data=yaml.safe_load(f)

   logger.info(f"{Path(__file__).name}: reading {config} file")

   def dictToNamespace(d):
     if isinstance(d,dict):
       return SimpleNamespace(**{k:dictToNamespace(v) for k,v in d.items()})
     elif isinstance(d,list):
       return [dictToNamespace(i) for i in d]
     else:
       return d
    
   return dictToNamespace(data)
      
ts=datetime.now()

def returnDemoDataByDifficulty():
    data={
       "userId":"agampatel@gmail.com",
        "testType":"testByDifficulty",
        "timeStamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "params":{
                  "difficultyLevel":["easy", "medium"],
                  "dataStructure":["array", "string"],
                  "companies":[],
                  "timeLimit":"None",
                  "numberOfQuestions":8,
                  "seed":48,
                  }
    }
    return data


def returnDemoDataByCompanies():
    data={
       "userId":"agampatel@gmail.com",
        "testId":12356442,
        "testType":"testByCompanies",
        "timeStamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "params":{
                  "difficultyLevel":["easy", "medium"],
                  "dataStructure":[],
                  "companies":["Flipkart", "Amazon"],
                  "timeLimit":"None",
                  "numberOfQuestions":8,
                  "seed":48,
                  }
    }
    return data
