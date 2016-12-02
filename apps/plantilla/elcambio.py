from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient('mongodb://mongouser:1234@localhost:27017/grupo14')
db = client.grupo14
a=db.pertemas.aggregate([{"$match":{"cuenta":"@piedadcordoba"}},{"$group":{"_id":None, "count":{"$sum":1}} }])

for p in a :
	print p


'''
aggregate({"$match":{"cuenta":"@piedadcordoba"}},{"$group": {"_id":{'f': "$fecha", 'f':"$followers"}}}) 
pipe = [{'$group': {'_id': None, 'total': {'$sum': '$goals'}}}]
db.goals.aggregate(pipeline=pipe)
'''

'''
results = db.ProductSalesPlan.aggregate([{ '$group':{'_id': { '$year': "$date" },'sale': {'$sum': '$sales' }}}])



db.contest.aggregate([
    {"$group" : {_id:"$province", count:{$sum:1}}}
])
'''