import logging.handlers
import types

_LOG_LEVEL = types.MappingProxyType(
    {
        "debug": logging.DEBUG,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "error": logging.ERROR,
        "fatal": logging.FATAL,
        "critical": logging.CRITICAL,
    }
)


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
        help="default is '%(default)s'",
    )

    parser.add_argument(
        "--log-datefmt", default="%Y-%m-%d %H:%M:%S", help="default is '%(default)s'"
    )

    destination_group = parser.add_mutually_exclusive_group()
    destination_group.add_argument(
        "--log-syslog",
        metavar="FACILITY",
        choices=logging.handlers.SysLogHandler.facility_names,
        help="Log into syslog",
    )
    destination_group.add_argument(
        "--log-none", action="store_true", help="Disable logging"
    )
    destination_group.add_argument("--log-file", help="Log into LOG_FILE")
    destination_group.add_argument(
        "--log-console", action="store_true", help="Log into console"
    )


def init_logging(namespace, default_handler=None):
    log_level = _LOG_LEVEL[namespace.log_level]

    formatter = logging.Formatter(namespace.log_format, datefmt=namespace.log_datefmt)

    handler = _create_handler(namespace) or default_handler or logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(log_level)


def _create_handler(namespace):
    if namespace.log_none:
        return logging.NullHandler()

    if namespace.log_file:
        return logging.FileHandler(namespace.log_file)

    if namespace.log_syslog:
        return create_syslog_handler(namespace.log_syslog)

    if namespace.log_console:
        return logging.StreamHandler()

    return None


def create_syslog_handler(facility="user", address="/dev/log"):
    facility = logging.handlers.SysLogHandler.facility_names[facility]
    return logging.handlers.SysLogHandler(facility=facility, address=address)
