from dataclasses import dataclass

@dataclass
class testByDifficultyConfig:
    difficultyLevel: list
    dataStructure: list
    numberOfQuestions: int
    excelPath: str
    seed:int

@dataclass
class testByCompaniesConfig:
    companies: list
    difficultyLevel: list
    numberOfQuestions: int
    excelPath: str
    seed: int

@dataclass
class testByGenAIConfig:
    numberOfQuestions: int
    difficultyLevel: int
    dataStructure: list

@dataclass
class databaseTestInitConfig:
    userId:str
    testId:str
    testType:str
    timeStamp:str

@dataclass
class databaseTestDetailsConfig:
    userId:str
    testId:str
    numberOfQuestions:int
    companies:list
    dataStructures:list
    difficultyLevel:list
    timeLimit:str

@dataclass
class databaseQuestionDetailsConfig:
    userId:str
    testId:set
    questionIds:dict
