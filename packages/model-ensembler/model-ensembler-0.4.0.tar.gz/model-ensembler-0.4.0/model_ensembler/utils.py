import logging
import logging.handlers
import os
import resource
import sys


# Should have used a collection for this
class Arguments(object):
    class __Arguments(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    instance = None

    def __init__(self, **kwargs):
        if not Arguments.instance:
            Arguments.instance = Arguments.__Arguments(**kwargs)

    def __getattr__(self, item):
        return getattr(self.instance, item)


def background_fork(double=False):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print("Fork failed: {} ({})".format(e.errno, e.strerror))
        sys.exit(1)

    os.setsid()

    if double:
        background_fork()


def setup_logging(name='',
                  level=logging.INFO,
                  verbose=False,
                  logdir=os.path.join("logs"),
                  logformat="[%(asctime)-20s :%(levelname)-8s] - %(message)s",
                  ):
    if verbose:
        level = logging.DEBUG

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    logging.basicConfig(
        level=level,
        format=logformat,
        datefmt="%d-%m-%y %T",
    )

    if logdir:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            os.path.join(logdir, "{}.log".format(name)),
            when='midnight',
            utc=True
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            fmt='%(asctime)-25s%(levelname)-17s%(message)s',
            datefmt='%H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)
