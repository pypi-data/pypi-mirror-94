import json

class DB:
    def __init__(self, path):
        self.path = path
        self.raw_json = open(self.path, 'w')
        self.db = json.load(open(self.path, 'r'))
    
    async def setval(self, key, val):
        self.db[key] = val
        json.dump(self.db, self.raw_json, indent=4)
    
    async def getval(self, key):
        return self.db[key]
    
    async def removeval(self, key):
        del self.db[key]
        json.dump(self.db, self.raw_json, indent=4)

def db(path:str):
    return DB(path)
