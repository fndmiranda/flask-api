import crypt
from pymongo import ReturnDocument
from app.database import get_db
from app.helpers import serialize_doc, serialize_filter


collection = 'users'


def get(filters={}, limit=25, page=1):
    """Retrieve all data by filters."""

    docs = get_db()[collection].find(serialize_filter(filters)).skip(limit * (page - 1))
    return serialize_doc(docs)


def find(filters={}):
    """Find one data by filters."""

    doc = get_db()[collection].find_one(serialize_filter(filters))
    return serialize_doc(doc)


def create(payload):
    """Save a new register."""

    if 'password' in payload:
        payload['password'] = crypt.crypt(payload['password'])

    doc = get_db()[collection].insert_one(payload)
    return find({'_id': doc.inserted_id})


def update(filters, payload):
    """Update data by filters."""

    if 'password' in payload:
        payload['password'] = crypt.crypt(payload['password'])

    doc = get_db()[collection].find_one_and_update(
        serialize_filter(filters), {'$set': payload}, return_document=ReturnDocument.AFTER
    )

    return serialize_doc(doc)


def delete(filters):
    """Delete data by filters."""

    doc = get_db()[collection].delete_one(serialize_filter(filters))
    return {'deleted_count': doc.deleted_count}
