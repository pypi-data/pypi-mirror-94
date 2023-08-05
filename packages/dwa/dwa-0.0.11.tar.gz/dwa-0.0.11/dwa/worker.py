import threading
import time
import traceback


class worker_example:
    terminate = False
    terminated = False
    exploded = False

    def job(self) -> None:
        pass

    def worker(self) -> None:
        while not self.terminate:
            try:
                self.job()
            except:
                traceback.print_exc()
                self.exploded = True
                break
        if self.terminate:
            self.terminated = True

    def stop(self) -> None:
        self.terminate = True
        while not self.terminated:
            time.sleep(1 / 1000)

    def start(self) -> None:
        p = threading.Thread(target=self.worker)
        p.daemon = True
        p.start()
