#!/usr/bin/env python3
"""
Get articles from the web
"""
import json
import socket
import sys
import scraping


def accept_status(status: bytes) -> bool:
    '''Check if the server status is OK'''
    if status == b'MSG-OK-DONE':
        return True

    if not status:
        raise InterruptedError('Server closed unexpectedly')
    elif not status.startswith(b'MSG-'):
        print(f'Unexpected response start: {status}', sys.stderr)
    elif not status.endswith(b'-DONE'):
        print(f'Unexpected response finish: {status}', file=sys.stderr)
    else:
        print(f'Problematic response {status}', file=sys.stderr)

    return False


# def recvall(connection: socket.socket, chunksize: int) -> bytes:
#     data = b''
#     while True:
#         recv_data = connection.recv(chunksize)
#         if not recv_data:
#             break
#         data += recv_data
#     return data


def add_length_header(data: bytes) -> bytes:
    length = str(len(data)).encode()
    header = (b'<length ' + length + b'>').ljust(32)
    return header + data


def consume_length_header(connection: socket.socket) -> int:
    raw_header = connection.recv(32)
    content_length = raw_header.strip(b'<length> ')
    return int(content_length)


def main():
    """
    Run the program
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(scraping.SOCKET_PATH)
        for i, client in enumerate(cls() for cls in scraping.API_CLIENTS):
            if 200 <= client.request() < 300:
                articles = client.results()
                print(articles, file=sys.stderr)

                try:
                    send_data = json.dumps(articles).encode()
                except json.JSONDecodeError:
                    print(f'Got bad json from {client.name}\n{send_data}',
                          file=sys.stderr)
                    continue

                max_attempts = 3
                while max_attempts > 0:
                    sock.sendall(add_length_header(send_data))
                    status_length = consume_length_header(sock)
                    status = sock.recv(status_length)

                    if accept_status(status):
                        break
                    max_attempts -= 1

                if max_attempts == 0:
                    print(f'Failed too many times, data=\n{send_data}',
                          sys.stderr)
                if i < len(scraping.API_CLIENTS) - 1:
                    sock.sendall(b'NEXT')
        sock.sendall(b'DONE')


if __name__ == '__main__':
    sys.exit(main())
