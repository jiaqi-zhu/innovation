import pymongo
from pymongo import MongoClient
import sys
# host = 'localhost'

class Agent:
	host = '10.3.13.177'
	port = 27017
	def __init__(self, dbname, host=host, port=port):
		try:
			self._conn = MongoClient(host, port)
			print 'connected to DB'
		except pymongo.errors.ConnectionFailure as e:
			print e
			sys.exit(-1)

		try:
			self._db = self._conn[dbname]
		except pymongo.errors.InvalidName as e:
			print e
			sys.exit(-1)

	def get_channel_list(self):
		return self._db.collection_names()

	def add_channel(self, channel, tv_channel=None, radio_freq=None):
		try: 
			self._db.create_collection(channel)
			col = getattr(self._db, channel)
			col.insert({'tv': tv_channel, 'radio': radio_freq})
		except pymongo.errors.CollectionInvalid:
			print '{} channel already exits'.format(channel)

	def update_channel_info(self, channel, type_, freq):
		col = getattr(self._db, channel)
		date = {type_: freq}
		col.update({}, {"$set": {type_: freq}}, upsert=True)

	def delete_channel(self, channel):
		self._db.drop_collection(channel)

	def get_data_from_collection(self, collection):
		col = getattr(self._db, collection)
		return list(col.find())[0]

	def get_channel(self, channel, type_):
		c = getattr(self._db, channel)
		return list(c.find({}, {type_: 1, '_id':0}))[0][type_]

	def get_channel_name_from_freq(self, radio_freq):
		for channel in self.get_channel_list():
			if self._db.channel.find({}, {"radio" : radio_freq}):
				return channel 

# if __name__ == '__main__':
	# db = Agent('innovation')
	# print db.get_channel_name_from_freq('88.5FM')
	# db.add_channel('tsn', tv_channel=62, radio_freq='54.9FM')
	# db.delete_channel('ABC')
	# print db.get_channel_list()
	# db.update_channel_info('rds', 'radio', '88.6FM')
	# print db.get_data_from_collection('rds')
	# print db.get_channel('cbc', 'radio')

	


