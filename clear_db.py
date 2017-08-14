from configuration import * #HAS ALL IMPORTANT STUFF LIKE PASSWORD AND USERNAMES
from pymongo import MongoClient

def destroy():
	conn = MongoClient(MONGO_ADDRESS)              # Mongo Stuff
	conn.admin.authenticate(MONGO_USERNAME, MONGO_PASSWORD)
	db = conn.travel
	collection = db.users
	db.users.delete_many({})
	print 'deleted_db;Waiting for Fresh entries!'

if __name__=='__main__':
	destroy()
