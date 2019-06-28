import cfg
import discord_bot
import threading
from twitch import TwitchClient

client = TwitchClient(cfg.client_id)


class GatherStreams:
    def __init__(self, queue):
        self.q = queue
        self.cache = list()
        self.start = True
        self.current_streams = []
        self.new_streams = []

    def set_queue(self, queue):
        self.q = queue

    def put(self, value):
        if self.q == -1:
            print(value)
            self.cache.append(value)
        elif self.q != -1 and self.start:
            self.start = False
            for v in self.cache:
                self.q.put(v)
            self.q.put(value)
        else:
            self.q.put(value)

    def reset_new_streams(self):
        self.new_streams = []

    def append_new_streams(self, element):
        self.new_streams.append(element)
        if element not in self.current_streams:
            self.put(element)

    def update_current_streams(self):
        self.current_streams = self.new_streams


gather_streams = GatherStreams(-1)


def process_stream_list(stream_list):
    for stream_entry in stream_list:
        #stream_entry = stream_entry["channel"]["url"]
        stream_entry = get_chat_string(stream_entry)
        gather_streams.append_new_streams(stream_entry)


def get_chat_string(stream_entry):
    return stream_entry["channel"]["display_name"] + " is currently playing " + stream_entry["game"] + "\nstatus: \n" + stream_entry["channel"]["status"] + "\n" + stream_entry["channel"]["url"]
    #stream_entry[""]


def start_gathering(queue):
    gather_streams.set_queue(queue)
    e = threading.Event()
    while not e.wait(cfg.interval):
        gather_streams.reset_new_streams()
        for game_name in cfg.game_names:
            process_stream_list(client.streams.get_live_streams(game=game_name))
        gather_streams.update_current_streams()
