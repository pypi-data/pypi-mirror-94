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
    # ! TEST EFFECT WITH OTHERS LIBRARY
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)


BASE_FORMAT = '[%(levelname)s]'
DEFAULT_FORMAT = BASE_FORMAT + ' %(message)s'


def setup_logging(
    *args,
    default_level=logging.WARNING,
    extend_format: str = None,
        **kwargs):
    """clean all default lambda logger handler, and setup bb logger \n
    default_level = logging.{INFO|WARNING|..} https://docs.python.org/3/library/logging.html#levels \n
    BASE_FORMAT = '[%(levelname)s]' \n
    DEFAULT_FORMAT = BASE_FORMAT + ' %(message)s'\n
    if extend_format is specified, FORMAT will be : BASE_FORMAT + '\\t'+ extend_format \n
    else DEFAULT_FORMAT wil be used  
    """

    remove_all_handlers()

    # setup format
    format = DEFAULT_FORMAT
    if extend_format:
        format = BASE_FORMAT + '\t' + extend_format
    logging.basicConfig(format=format, level=default_level)
    # add custom level
    _add_logger_level('NOTI', logging.WARNING + 5)

    # set log level
