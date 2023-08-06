from os import environ, set_inheritable, unsetenv
from socket import socket
from itertools import zip_longest
from public import public
from itertools import groupby

SD_LISTEN_FDS_START = 3


def by_name(fd_desc):
    name, fd = fd_desc
    return name


@public
def get_sockets_from_fds() -> dict[str, tuple[socket]]:
    """
        Returns a dictionary of lists of sockets passed down by systemd.
            Multiple calls to this function will return the same socket
            objects when called in the same python interpreter.
            This will delete the environment variables, and make
            the file descriptors non-inheritable.
    """
    try:
        num_of_sockets = int(environ['LISTEN_FDS'])
        # We use unsetenv so that environ will keep them, but
        # subprocesses will not see the values
        unsetenv('LISTEN_FDS')
    except KeyError:
        return {}

    names = filter(
        lambda name: name,
        environ.get('LISTEN_FDNAMES', '').split(':'),
    )
    unsetenv('LISTEN_FDNAMES')

    fds = tuple(
        range(SD_LISTEN_FDS_START, num_of_sockets + SD_LISTEN_FDS_START)
    )

    for fd in fds:
        set_inheritable(fd, False)

    fds_with_names = zip_longest(names, fds, fillvalue='unknown')
    sorted_fds = sorted(fds_with_names, key=by_name)

    sockets_by_name = (
        (name, tuple(socket(fileno=fd) for name, fd in fds if fd != 'unknown'))
        for name, fds in groupby(sorted_fds, key=by_name)
    )

    return {
        name: sockets
        for name, sockets in sockets_by_name
        if sockets
    }
