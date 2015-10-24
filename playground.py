from dataobjects.collection import Collection
import json

col = Collection()
col.fill_collection_empty()
print json.dumps(col.cards)
