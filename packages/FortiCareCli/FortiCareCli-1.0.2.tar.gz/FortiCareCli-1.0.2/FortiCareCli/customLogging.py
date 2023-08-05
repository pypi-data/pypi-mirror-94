# vim: tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab

import logging
import sys

class CustomLogFormatter(logging.Formatter):
    '''
    The CustomLogFormatter is very similar to default Formatter,
    but in case of multi-line messages, it prints the header
    at the beggining of each line (unlike the default Formatter).
    '''

    def __init__(self):
        logging.Formatter.__init__(self, "[%(asctime)s] %(message)s", '%Y-%m-%d %H:%M:%S')

    def format(self, record):
        logging.Formatter.format(self, record)
        message = record.getMessage()

        # write header at the beggining of every line
        out = ""
        for line in message.split("\n"):
            out += "[{}] ({}) {}\n".format(record.asctime, record.levelname, line)

        # do not finish with new line - it will be added automatically
        if out[-1] == "\n": out = out[:-1]
        return out


def setup(logMinLevel):
    '''
    Initialize the Python logging system.
    :param logMinLevel: Log level from logging module (like logging.INFO). This and higher will be printed.
    '''

    handler_stdout = logging.StreamHandler(sys.stdout)
    handler_stdout.setFormatter(CustomLogFormatter())
    logging.basicConfig(
        level   = logMinLevel,
        handlers = [
            handler_stdout
        ]
    )
