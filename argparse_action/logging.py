import enum
import logging.handlers
import types

_LOG_LEVEL = types.MappingProxyType({
    "debug":  logging.DEBUG,
    "warning":  logging.WARNING,
    "info":  logging.INFO,
    "error":  logging.ERROR,
    "fatal":  logging.FATAL,
    "critical":  logging.CRITICAL,
})


def add_log_arguments(parser):
    parser.add_argument(
        "--log-level",
        choices=_LOG_LEVEL,
        default="info",
        help="default is '%(default)s'",
    )

    parser.add_argument(
        "--log-format",
        default="%(asctime)s %(name)s %(levelname)s %(message)s",
        help="default is '%(default)s'"
    )

    parser.add_argument(
        "--log-datefmt",
        default="%Y-%m-%d %H:%M:%S",
        help="default is '%(default)s'"
    )

    destination_group = parser.add_mutually_exclusive_group()
    destination_group.add_argument(
        "--log-syslog",
        metavar="FACILITY",
        choices=logging.handlers.SysLogHandler.facility_names,
        help="Log into syslog"
    )
    destination_group.add_argument(
        "--log-none",
        action="store_true",
        help="Disable logging"
    )
    destination_group.add_argument(
        "--log-file",
        help="Log into LOG_FILE"
    )


def init_logging(namespace):
    log_level = _LOG_LEVEL[namespace.log_level]

    formatter = logging.Formatter(namespace.log_format, datefmt=namespace.log_datefmt)

    handler = _create_handler(namespace)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(log_level)


def _create_handler(namespace):
    if namespace.log_none:
        return logging.NullHandler()

    elif namespace.log_file:
        return logging.FileHandler(namespace.log_file)

    elif namespace.log_syslog:
        facility = logging.handlers.SysLogHandler.facility_names[namespace.log_syslog]
        return logging.handlers.SysLogHandler()

    return logging.StreamHandler()
