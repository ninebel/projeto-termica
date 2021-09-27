# user: admin
# password: rKh2w5f8O4pJjBBM

from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb+srv://admin:rKh2w5f8O4pJjBBM@cluster0.xhzav.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db=client.furnaces # select 'furnaces' as db name
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

test = {'Hello':'Chill mate, just testinn'}
result=db['hai.test'].insert_one(test) # reviews is the collection name
result=db.reviews2.insert_one(test)

fivestar = db['hai.test'].find_one({'Hello':'Chill mate, just testinn'})
print(fivestar)
