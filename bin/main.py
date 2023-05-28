from network import *

from lib.server import VideoServer
from lib.client import VideoClient
from lib.thread import get_threads

class VideoCollection:
    def __init__(self):
        print("Initializing...")
        self.server = VideoServer(port=8002, collection=self)
        self.cameras = get_threads(collection=self)
        self.client = VideoClient(collection=self)
        
    def start(self):
        print("Starting threads...")
        server_thread = ServerThread(self.server)
        ServerThread.startThreads([server_thread, *self.cameras.values()])

if __name__ == '__main__':
    collection = VideoCollection()
    collection.start()
