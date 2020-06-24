""" starcli.terminal_size """


def terminal_size():
    """ Fetches the terminal size and returns it """
    import fcntl, termios, struct

    th, tw, hp, wp = struct.unpack(
        "HHHH", fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0))
    )
    return tw, th
