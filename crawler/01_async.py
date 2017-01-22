import socket
from selectors import DefaultSelector, EVENT_WRITE

from crawler.logger import log


def run_sync():
    log("\nRunning synchronously with busy-waiting\n")
    sock = create_socket()
    request = "GET xkcd.com HTTP/1.0\r\nHost: xkcd.com\r\n\r\n"
    encoded = request.encode("ascii")
    wait_for_socket_in_a_loop(encoded, sock)
    log("Ready!")


def run_async():
    log("\nRunning asynchronously with a simple event loop\n")
    sock = create_socket()
    wait_for_socket_async(sock)
    log("Ready!")


def create_socket():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        log("Connect")
        sock.connect(("xkcd.com", 80))
        log("After connect")
    except BlockingIOError as e:
        log(f"Caught: {e}")
    log("After try")
    return sock


def wait_for_socket_in_a_loop(encoded, sock):
    while True:
        try:
            sock.send(encoded)
            break
        except OSError as e:
            log(f"Error: {e}")


def wait_for_socket_async(sock):
    selector = DefaultSelector()

    def connected():
        selector.unregister(sock.fileno())
        log("Connected!")

    selector.register(sock.fileno(), EVENT_WRITE, connected)
    loop(selector)


def loop(selector):
    log("Starting event loop")
    while True:
        log("Waiting for events...")
        events = selector.select()
        log("Got event!")
        for event_key, event_mask in events:
            callback = event_key.data
            callback()
        break
    log("Exiting event loop")


if __name__ == '__main__':
    run_sync()
    run_async()
