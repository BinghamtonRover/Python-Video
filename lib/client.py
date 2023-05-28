import threading
import time

from network.generated import *

class VideoClient(threading.Thread):
    def __init__(self, collection):
        self.collection = collection
        self.keep_alive = True
        super().__init__()

    def run(self):
        while self.keep_alive:
            for thread in self.collection.cameras:
                self.collection.server.send_message(VideoData(
                    id=thread.camera_id,
                    details=thread.details,
                ))

    def close(self): self.keep_alive = False
