import threading
import time


class ThreadManager:
    def __init__(self):
        self.__opened_threads = {}
        self.__is_running = True
        self.__wait_time = 60000
        thread = threading.Thread(target=self.dying_light)
        self.add_thread(thread, "Zombie Killer")

        thread.start()

    def add_thread(self, thread: threading.Thread, name: str):
        """Add a new thread to the manager"""
        self.__opened_threads[thread] = name

    def dying_light(self):
        """Kill the zombies using thread parkour (^u^)/"""

        while self.__is_running:
            # Get the possible zombies
            threads = self.__opened_threads.keys()

            # Make some zombie test
            for thread in threads:
                if not thread.is_alive():
                    # Kill the zombie!
                    self.__opened_threads.pop(thread)

            time.sleep(self.__wait_time)

        self.__opened_threads = {}
