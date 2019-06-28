import twitter
import discord_bot
import twitch_reader
import multiprocessing
from threading import Thread


if __name__ == "__main__":
	q1 = multiprocessing.Queue()
	q2 = multiprocessing.Queue()
	thread_1 = Thread(target=discord_bot.access_queue, args=(q1, q2))
	thread_1.start()
	thread_2 = Thread(target=twitter.populate_queue, args=(q1,))
	thread_2.start()
	thread_3 = Thread(target=twitch_reader.start_gathering, args=(q2,))
	thread_3.start()
