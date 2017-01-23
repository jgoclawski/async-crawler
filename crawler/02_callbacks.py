import selectors
import socket

from crawler.logger import log

urls_todo = {'/'}
seen_urls = {'/'}
selector = selectors.DefaultSelector()
stopped = False


class Fetcher:
    def __init__(self, url):
        self.response = b''  # Empty array of bytes.
        self.url = url
        self.sock = None

    def fetch(self):
        log(f"Creating socket ({self.url})")
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('xkcd.com', 80))
        except BlockingIOError:
            pass

        # Register next callback.
        selector.register(self.sock.fileno(),
                          selectors.EVENT_WRITE,
                          self.connected)

    def connected(self, key, mask):
        log(f"Connected! ({self.url})")
        selector.unregister(key.fd)
        request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(self.url)
        self.sock.send(request.encode('ascii'))

        # Register the next callback.
        selector.register(key.fd,
                          selectors.EVENT_READ,
                          self.read_response)

    def read_response(self, key, mask):
        log(f"Read response ({self.url})")
        global stopped

        chunk = self.sock.recv(4096)  # 4k chunk size.
        if chunk:
            log(f"Got chunk ({self.url})")
            self.response += chunk
        else:
            log(f"Done reading ({self.url})")
            selector.unregister(key.fd)  # Done reading.
            links = self.parse_links()

            for link in links.difference(seen_urls):
                urls_todo.add(link)
                log(f"Adding link {self.url} -> {link}")
                Fetcher(link).fetch()  # <- New Fetcher.

            seen_urls.update(links)
            urls_todo.remove(self.url)
            if not urls_todo:
                log(f"No more links to process ({self.url})")
                stopped = True

    def parse_links(self):
        if self.url == '/':
            return {
                '/353/',
                '/354/',
                '/355/',
            }
        else:
            return {
                '/123/',
                '/456/',
            }


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)

if __name__ == '__main__':
    fetcher = Fetcher('/')
    fetcher.fetch()
    loop()
