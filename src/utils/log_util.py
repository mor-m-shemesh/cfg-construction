import logging


def make_logger(stdout: bool = False, filepath: str = None):
    """
    Get dual-logger - for file+stdout logging

    :param stdout: Whether to output log (Info level) to stdout
    :param filepath: If given, saves log (Debug level) to file in filepath
    :return: logging.Logger object with the requested params
    """
    log = logging.getLogger('logger')
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(message)s')

    if stdout:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        log.addHandler(ch)

    if filepath:
        fh = logging.FileHandler(filepath, encoding='ascii')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    return log