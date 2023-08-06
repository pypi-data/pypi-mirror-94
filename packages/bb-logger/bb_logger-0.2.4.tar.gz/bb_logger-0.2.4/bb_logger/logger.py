import logging


def _add_logger_level(levelname, level, *, func_name=None):
    """

    :type levelname: str
        The reference name of the level, e.g. DEBUG, WARNING, etc
    :type level: int
        Numeric logging level
    :type func_name: str
        The name of the logger function to log to a level, e.g. "info" for log.info(...)
    """

    func_name = func_name or levelname.lower()

    setattr(logging, levelname, level)
    logging.addLevelName(level, levelname)
    _func_prototype = "def {logger_func_name}(self, message, *args, **kwargs):\n" \
        "    if self.isEnabledFor({levelname}):\n" \
        "        self._log({levelname}, message, args, **kwargs)"

    exec(
        _func_prototype.format(
            logger_func_name=func_name,
            levelname=levelname),
        logging.__dict__,
        locals())
    setattr(logging.Logger, func_name, eval(func_name))


def remove_all_handlers():
    """remove all current handlers
    """
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)


BASE_FORMAT = '[%(levelname)s] [%(noti_status)s]'
DEFAULT_FORMAT = BASE_FORMAT + ' %(message)s'


def setup_logging(
    *args,
    default_level=logging.WARNING,
    extend_format: str = None,
    default_noti_level=logging.ERROR,
    force_noti_level=logging.CRITICAL,
        **kwargs):
    """clean all default lambda logger handler, and setup bb logger \n
    default_level = logging.{INFO|WARNING|..} https://docs.python.org/3/library/logging.html#levels \n
    BASE_FORMAT = '[%(levelname)s]' \n
    DEFAULT_FORMAT = BASE_FORMAT + ' %(message)s'\n
    if extend_format is specified, FORMAT will be : BASE_FORMAT + '\\t'+ extend_format \n
    else DEFAULT_FORMAT wil be used \n
    default_noti_level= logging.ERROR \n,
    all log from this level will be noticed if no arguments are provided
    force_noti_level = logging.{INFO|WARNING|..} \n
    force all log with this level be noticed, ignore arguments
    """

    remove_all_handlers()

    # add logic handler
    # noti
    class NotiFormatter(logging.Formatter):
        def format(self, record):
            if(record.args and isinstance(record.args, dict) and 'noti' in record.args.keys()):
                noti = record.args.get("noti")
                record.noti_status = "NOTI" if noti else 'NOT_NOTI'
            else:
                record.noti_status = 'NOTI' if record.levelno >= default_noti_level else 'NOT_NOTI'

            if record.levelno >= force_noti_level:
                record.noti_status = 'NOTI'

            return super().format(record)
    # setup format
    format = DEFAULT_FORMAT
    if extend_format:
        format = BASE_FORMAT + '\t' + extend_format
    noti_ch = logging.StreamHandler()
    noti_ch.setFormatter(NotiFormatter(format))
    logging.basicConfig(level=default_level, handlers=[noti_ch])

    # add custom level
    # _add_logger_level('NOTI', logging.WARNING + 5) # user info and force
    # noti instead

    # set log level


def setup_logging_dec(*args,
                      default_level=logging.WARNING,
                      extend_format: str = None,
                      lambda_exec_error_log=True,
                      default_noti_level=logging.ERROR,
                      force_noti_level=logging.CRITICAL,
                      **kwargs):
    """decorator setup logging for lambda

    Args:
        default_level (int, optional): min log level. Defaults to logging.WARNING.
        extend_format (str, optional): custom extend format. Defaults to None.
        lambda_exec_error_log (bool, optional): log with critical level for lambda raise exception. Defaults to True.
        default_noti_level(int, optional): all log from this level will be noticed if no arguments are provided. Defaults to logging.ERROR.
        force_noti_level (int, optional): force all log with this level to be noticed. Defaults to logging.CRITICAL.
    """
    def inner(func):
        def wrapper(*args, **kwargs):
            setup_logging(
                default_level=default_level,
                extend_format=extend_format,
                default_noti_level=default_noti_level,
                force_noti_level=force_noti_level)
            try:
                func(*args, **kwargs)
            except Exception as e:
                if lambda_exec_error_log:
                    logging.critical(str(e), exc_info=True)
                raise e

        return wrapper

    return inner
