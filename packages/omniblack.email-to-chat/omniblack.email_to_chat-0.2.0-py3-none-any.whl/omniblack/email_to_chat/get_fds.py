from os import environ
from socket import socket
from itertools import zip_longest
from logging import getLogger

log = getLogger(__name__)

SD_LISTEN_FDS_START = 3


def get_sockets_from_fds():
    sockets = {}
    num_of_sockets = int(environ['LISTEN_FDS'])
    names = environ['LISTEN_FDNAMES'].split(':')

    for name, fd in zip_longest(
            names,
            range(SD_LISTEN_FDS_START, num_of_sockets + SD_LISTEN_FDS_START),
            fillvalue='unknown',
    ):
        if name == 'unknown':
            sockets.setdefault(name, [])
            sockets[name].append(socket(fileno=fd))
        elif name not in sockets:
            sockets[name] = socket(fileno=fd)

    return sockets
