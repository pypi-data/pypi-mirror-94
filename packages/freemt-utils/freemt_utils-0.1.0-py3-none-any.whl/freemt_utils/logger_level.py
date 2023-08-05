'''
set logger level of loguru DEBUG INFO
'''
# pylint: disable=broad-except

# import sys
# from loguru import logger
import logzero


def logger_level(level: str = 'DEBUG') -> None:
    ''' set logger level'''
    _ = """
    try:
        logger.remove()  # noqa
        logger.add(sys.stderr, level=level.upper())  # noqa
    except Exception:
        print(sys.exc_info()[:2])
    """
    if level.lower in ["debug", "10"]:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)
