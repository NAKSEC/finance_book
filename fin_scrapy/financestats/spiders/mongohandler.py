import pymongo
from pymongo import MongoClient


def connect(address, lazy_connection=False):
    """Set up a connection to the MongoDB server.

    Parameters:
        address: MongoDB server address.
        lazy_connection: avoid testing if the connection is working while
            initializing it.
    """
    try:
        print "connect"
        client = MongoClient(address)
    except Exception as e:
        print e

    # Send a query to the server to see if the connection is working.
    try:
        print "server info"
        client.server_info()
    except Exception as e:
        print ("Unable to connect to %s.", e)
        client = None
    return client


def mongo_insert(data):
    print "in handler"
    client = connect('mongodb://localhost:27017/', False)
    print "connected /r/n "
    db = client['stocks']
    try:
        result = db.Stats.insert_one(data)
        print "Result %s, objectId : %s" % (result.acknowledged, result.inserted_id)
    except pymongo.results.InsertOneResult as e:
        return
    print "data inserted"
