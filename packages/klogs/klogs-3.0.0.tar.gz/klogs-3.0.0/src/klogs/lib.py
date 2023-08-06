import contextlib
import logging
import sys


SHORT_FORMATTER = logging.Formatter(
    "[%(asctime)s:%(levelname)s:%(name)s:%(funcName)s]: "
    "%(message)s"
)

LONG_FORMATTER = logging.Formatter(
    "[%(asctime)s:%(levelname)s:%(name)s:%(funcName)s] "
    "{%(filename)s:%(lineno)s} %(message)s"
)


class ExcludeFilter:

    def __init__(self, excludes):
        self.excludes = excludes

    def filter(self, record):
        return record.name not in self.excludes


def create_handler(
    *,
    with_line_no=False,
    level=None,
    log_file=None,
    file_mode=None,
    excludes=None,
):
    level = logging.INFO if level is None else level
    file_mode = "w" if file_mode is None else file_mode
    excludes = [] if excludes is None else excludes

    if log_file is None:
        log_handler = logging.StreamHandler(sys.stdout)
    else:
        log_handler = logging.FileHandler(log_file, mode=file_mode)

    if excludes:
        log_handler.addFilter(ExcludeFilter(excludes))

    formatter = LONG_FORMATTER if with_line_no else SHORT_FORMATTER
    log_handler.setFormatter(formatter)

    return log_handler


def configure_logging(
    *,
    with_line_no=None,
    level=None,
    log_file=None,
    file_mode=None,
    excludes=None,
):

    logging.getLogger().setLevel(level)
    logging.getLogger().addHandler(create_handler(
        with_line_no=with_line_no,
        level=level,
        log_file=log_file,
        file_mode=file_mode,
        excludes=excludes,
    ))


@contextlib.contextmanager
def push_log_configuration(
    *,
    with_line_no=None,
    level=None,
    log_file=None,
    file_mode=None,
    excludes=None,
):
    logger = logging.getLogger()
    old_level = logger.level
    handler = create_handler(
        with_line_no=with_line_no,
        level=level,
        log_file=log_file,
        file_mode=file_mode,
        excludes=excludes,
    )
    try:
        logger.setLevel(level)
        logger.addHandler(handler)
        yield
    finally:
        logger.removeHandler(handler)
        logger.setLevel(old_level)
