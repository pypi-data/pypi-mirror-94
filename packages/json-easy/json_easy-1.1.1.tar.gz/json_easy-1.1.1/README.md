# json-easy
Used to make json db'ing easier

Usage:
```py
import json-easy as json
db = json.db('path/to/db.json')
#in a function
await db.changeval('somekey', 'someval')
await db.getval('somekey')
await db.removeval('somekey')
```
