import logging
import colorlog

logger = logging.getLogger()


def setup_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt="[%(asctime)s]%(log_color)s %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "black",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bold",
            },
            datefmt="%Y-%m-%d %H:%M:%S",
        ),
    )

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
