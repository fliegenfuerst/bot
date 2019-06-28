import tweepy
import cfg


class QueueHandler:
	def __init__(self, queue):
		self.q = queue
		self.cache = list()
		self.start = True

	def set_queue(self, queue):
		self.q = queue

	def put(self, value):
		if self.q == -1:
			self.cache.append(value)
		elif self.q != -1 and self.start:
			self.start = False
			for v in self.cache:
				self.q.put(v)
			self.q.put(value)
		else:
			self.q.put(value)


queue_handler = QueueHandler(-1)


class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		if str(status.user._json["id"]) in cfg.accounts:
			queue_handler.put("https://twitter.com/"+status.user._json["screen_name"]+"/status/"+str(status.id))

	def on_error(self, status_code):
		if status_code == 420:
			print("Error 420")


auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
api = tweepy.API(auth)
my_stream_listener = MyStreamListener()
my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)


def populate_queue(queue):
	queue_handler.set_queue(queue)
	#my_stream.filter(track=cfg.keywords, is_async=False)
	my_stream.filter(follow=cfg.accounts, is_async=False)