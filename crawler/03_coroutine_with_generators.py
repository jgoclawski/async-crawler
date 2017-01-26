import selectors
import socket

from crawler.logger import log

selector = selectors.DefaultSelector()
stopped = False


class Fetcher:
    def __init__(self, url):
        self.response = b''  # Empty array of bytes.
        self.url = url

    def fetch(self):
        log(f"Fetcher :: Fetch started ({self.url})")
        log(f"Fetcher :: Creating socket ({self.url})")
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('xkcd.com', 80))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected():
            log(f"Fetcher :: Socket connected ({self.url})")
            f.set_result(None)

        selector.register(sock.fileno(),
                          selectors.EVENT_WRITE,
                          on_connected)
        log(f"Fetcher :: Before sleeping ({self.url})")
        yield f
        log(f"Fetcher :: After sleeping ({self.url})")
        log(f"Fetcher :: Unregistering from selector ({self.url})")
        selector.unregister(sock.fileno())

        request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(self.url)
        sock.send(request.encode('ascii'))

        while True:
            f = Future()

            def on_readable():
                log(f"Fetcher :: Socket received data ({self.url})")
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(),
                              selectors.EVENT_READ,
                              on_readable)
            log(f"Fetcher :: Before sleeping ({self.url})")
            chunk = yield f
            log(f"Fetcher :: After sleeping ({self.url})")
            log(f"Fetcher :: Unregistering from selector ({self.url})")
            selector.unregister(sock.fileno())
            if chunk:
                log(f"Fetcher :: Got chunk ({self.url})")
                self.response += chunk
            else:
                log(f"Fetcher :: Done reading ({self.url})")
                break

        global stopped
        stopped = True
        log(f"Fetcher :: Fetch finished ({self.url})")


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)
        log(f"Future :: add_done_callback - {self._callbacks}")

    def set_result(self, result):
        log(f"Future :: set_result - {result}, callbacks: {self._callbacks}")
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Task:
    def __init__(self, coroutine):
        log("Task :: init started")
        self.coroutine = coroutine
        f = Future()
        f.set_result(None)
        self.step(f)
        log("Task :: init finished")

    def step(self, future):
        log("Task :: step started")
        try:
            log("Task :: Coroutine - before send")
            next_future = self.coroutine.send(future.result)
            log("Task :: Coroutine - after send")
        except StopIteration:
            log("Task :: finished")
            return

        next_future.add_done_callback(self.step)
        log("Task :: step finished")


def loop():
    log("Loop :: started")
    while not stopped:
        events = selector.select()
        log("Loop :: selected")
        for event_key, event_mask in events:
            callback = event_key.data
            callback()
    log("Loop :: finished")

if __name__ == '__main__':
    fetcher = Fetcher('/353/')
    Task(fetcher.fetch())
    loop()
