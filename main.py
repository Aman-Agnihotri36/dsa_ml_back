



from src.utils.customLogger import logger
from src.utils import returnDemoDataByCompanies
from src.replies.testReplyFinal import testByCompaniesReplyFinal

data=returnDemoDataByCompanies()

one,two=testByCompaniesReplyFinal(data)
print(two)