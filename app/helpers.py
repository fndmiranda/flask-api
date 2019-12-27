from pymongo.cursor import Cursor
from bson.objectid import ObjectId


def serialize_doc(data):
    """Serialize document."""

    if data:
        if isinstance(data, Cursor):
            data = list(data)

        if isinstance(data, dict):
            data['id'] = str(data['_id'])
            del data['_id']
        elif isinstance(data, list):
            for doc in data:
                doc['id'] = str(doc['_id'])
                del doc['_id']
    return data


def serialize_filter(filters):
    """Serialize filters."""

    if '_id' in filters:
        filters.update({"_id": ObjectId(filters['_id'])})

    return filters
