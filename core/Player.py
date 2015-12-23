from gmusicapi import Mobileclient
import urllib2 # url decoding

class Player:
	def __init__(self,creds,logging=False,val=False,ssl=True):
		# verify that creds is a dict or raise TypeError
		if not (creds instanceof dict):
			raise TypeError('Credentials passed are not a dictionary')

		# verify that the fields for the dict are filled or raise Error
		if not (creds["email"] or creds["password"] or creds["mac"]):
			raise Error('Missing parameters for login')
		
		# create Mobileclient and set local variables
		self.email = creds["email"]
		self.password = creds["pass"]
		self.mac = creds["mac"]
		self.mc = Mobileclient(debug_logging=logging,validate=val,verify_ssl=ssl)
		
		# verify Mobileclient logged in or raise ConnectionError
		if not self.mc.login(self.email,self.password,self.mac):
			raise ConnectionError('Could not connect using those credentials')

	# search all playlists
	# if id is share_token, return list of songs in shared playlist
	# else if id, return list of songs in that playlist
	# else no id, and return get_playlists
	def get_playlist(self,id=None):
		if "http://play.google.com/music/playlist/" in id:
			return self.mc.get_shared_playlist_contents(urllib2.unquote(id))
		elif id:
			pl=[]
			playlists = self.mc.get_all_user_playlist_contents()
			for p in playlists:
				if(p['id']==id):
					pl.append(p)
			if len(pl)>0:
				return pl
				# default to get_playlists if empty
		return self.get_playlists()


	# returns list of dictionaries 
	# containing {'name':'EDM List','id':'id_number'}
	def get_playlists(self):
		return self.mc.get_all_playlists()


	# if query, search song and return mp3 file 
	# if no query, Feeling Lucky mix
	def get_song_by_query(self,query=None):
		if query:
			self.mc.search_all_access(query,max_results=10)

		
	# searches for song by id
	# if id is None, raise Error
	# else get_stream_url by id
	def get_song_by_id(self,id=None):
		return self.mc.get_stream_url(song_id=id)


	# create playlist and return id
	def create_playlist(self,name):
		

	# if id, add song id to playlist
	# if query, add returned id of get_song_by_query(query)
	# if no id/query, raise Error
	def add_to_playlist(self,id=None,query=None):
		if query and id:
			raise Error('Cannot search for id and query in same call')
		elif query:
			song = self.get_song_by_query(query)
		elif id:
			song = self.get_song_by_id()


	# this method should only be called if a song is playing 
	# returns list of song ids changed
	def rateSong(self,rating, id):
		song = self.mc.get_track_info(id)
		if rating is "up":
			song['rating'] = '5'
		elif rating is "down":
			song['rating'] = '1'
		else
			return
		return self.mc.change_song_metadata(song)

	# logout of Mobileclient and return success boolean
	def logout(self):
		return self.self.mc.logout():

	# set validate value in Mobileclient
	def setValidate(self,val=False):
		self.mc.validate=val

	# return validate value from Mobileclient
	def getValidate(self):
		return self.mc.validate

	# return email used for Mobileclient
	def getEmail(self):
		return self.email
