import discord
import cfg
import threading

client = discord.Client()


async def send_message(message, channel):
	await client.get_channel(channel).send(message)


class PostTweets:
	def __init__(self, queue):
		self.q = queue

	def set_queue(self, queue):
		self.q = queue

	async def look_for_and_post_tweets(self):
		if self.q != -1:
			while self.q.qsize() > 0:
				try:
					await send_message(self.q.get(), cfg.target_channel_id)
				except self.q.Empty:
					print("isEmpty")


post_tweets = PostTweets(-1)


class PostTwitchStreams:
	def __init__(self, queue):
		self.q = queue
		self.switcher = False

	def switch(self):
		self.switcher = not self.switcher
		return self.switcher

	def set_queue(self, queue):
		self.q = queue

	async def look_for_and_post_streams(self):
		if self.q != -1:
			while self.q.qsize() > 0:
				try:
					await send_message(self.q.get(), cfg.live_now_target_channel_id)
				except self.q.Empty:
					print("isEmpty")


post_twitch_streams = PostTwitchStreams(-1)


def access_queue(twitter_queue, twitch_queue):
	post_twitch_streams.set_queue(twitch_queue)
	post_tweets.set_queue(twitter_queue)
	client.run(cfg.token)


async def set_interval():
	e = threading.Event()
	while not e.wait(30):
		if post_twitch_streams.switch():
			await post_twitch_streams.look_for_and_post_streams()
		else:
			await post_tweets.look_for_and_post_tweets()


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	await set_interval()
	await client.change_presence(status=discord.Status('online'), afk=False)
