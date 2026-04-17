from dataclasses import dataclass

@dataclass
class solutionDetailsConfig:
    userId:str
    testId:str
    solutions:dict
    timeTaken:int
    excelPath:str

@dataclass
class databaseScoreConfig:
    userId:str
    testId:str
    score:int
    result:dict
