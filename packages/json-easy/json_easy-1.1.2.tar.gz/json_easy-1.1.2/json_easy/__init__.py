import json

class DB:
    def __init__(self, path):
        self.path = path
        self.raw_json_writable = open(self.path, 'w')
        self.raw_json = open(self.path, 'r')
        self.db = json.load(self.raw_json)
        self.raw_json.close()
    
    async def setval(self, key, val):
        self.db[key] = val
        json.dump(self.db, self.raw_json_writable, indent=4)
        await self.close()
    
    async def getval(self, key):
        return self.db.get(key) or None
    
    async def removeval(self, key):
        del self.db[key]
        json.dump(self.db, self.raw_json_writable, indent=4)
        await self.close()
    
    async def close(self):
        self.raw_json_writable.close()

def db(path:str):
    return DB(path)
