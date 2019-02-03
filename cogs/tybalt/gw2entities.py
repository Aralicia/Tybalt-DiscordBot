from enum import Enum
from .database import database
import aiohttp
import json

class EntityType(Enum):
    def item():
        return {'sql':'item', 'api':'items'}

class GW2Entities:
    def findById(self, id, type):
        database.verify_connection()
        cursor = database.get_cursor()
        query = ("SELECT api_id, name FROM entity WHERE type = %s AND api_id = %s and removed = 0")
        cursor.execute(query, (type['sql'], id))
        for (api_id, name) in cursor:
            return ([{'id': api_id, 'name': name}], 1)
        return ([], 0)

    def findByName(self, name, type, limit):
        database.verify_connection()
        cursor = database.get_cursor()
        query = ("SELECT SQL_CALC_FOUND_ROWS api_id, name, distance FROM (SELECT api_id, name, damlevlim(%s, name, 254) as `distance` FROM entity WHERE type = %s and removed = 0) t WHERE (distance < 3 OR name LIKE %s) ORDER BY IF(name LIKE %s,1,0) DESC, distance ASC LIMIT %s")
        pattern = '%'+name+'%'
        cursor.execute(query, (name, type['sql'], pattern, pattern, limit))
        results = [];
        for (api_id, name, distance) in cursor:
            results.append({'id': api_id, 'name': name, 'distance': distance})
        cursor.execute("SELECT FOUND_ROWS()");
        (total,) = cursor.fetchone();
        return (results, total)

gw2entities = GW2Entities()
