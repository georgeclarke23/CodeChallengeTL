import logging
import os
import traceback


class LoggingProvider:
    def __init__(self):
        self.format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.level = "DEBUG"
        self.loggers = {}
        self._show_source_location = False
        self._show_function = False

        if "LOG_FORMAT" in os.environ:
            self.format = os.environ["LOG_FORMAT"]
        if "LOG_LEVEL" in os.environ:
            self.level = os.environ["LOG_LEVEL"]

        # Remove pre-existing handlers on root logger (i.e. AWS handler on Lambda)
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)

    def __get_logger(self, name):
        if name not in self.loggers:
            logger = logging.getLogger(name)
            if not len(logger.handlers):
                # loggers are singletons so only config handler once
                formatter = logging.Formatter(self.format)
                handler = logging.StreamHandler()
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            logger.setLevel(self.level)
            self.loggers.update({name: logger})
            return logger
        else:
            return self.loggers[name]

    def set_level(self, level):
        for name in self.loggers:
            self.loggers[name].setLevel(level)

    def show_source_location(self, show):
        self._show_source_location = show

    def show_function(self, show):
        self._show_function = show

    # Formats the message as needed and calls the correct logging method
    # to actually handle it
    def _raw_log(self, logfn, message, exc_info):
        cname = ""
        loc = ""
        fn = ""
        tb = traceback.extract_stack()
        if len(tb) > 2:
            if self._show_source_location:
                loc = "(%s:%d) - " % (os.path.basename(tb[-3][0]), tb[-3][1])
            if self._show_function:
                fn = tb[-3][2]
                if fn != "<module>":
                    if self.__class__.__name__ != logging.Logger.__name__:
                        fn = self.__class__.__name__ + "." + fn
                    fn += "()"
                fn += " - "

        logfn(loc + cname + fn + message.replace("\n", "\r"), exc_info=exc_info)

    def info(self, name, message, exc_info=False):
        """
        Log a info-level message. If exc_info is True, if an exception
        was caught, show the exception information (message and stack trace).
        """
        logger = self.__get_logger(name)
        self._raw_log(logger.info, message, exc_info)

    def debug(self, name, message, exc_info=False):
        """
        Log a debug-level message. If exc_info is True, if an exception
        was caught, show the exception information (message and stack trace).
        """
        logger = self.__get_logger(name)
        self._raw_log(logger.debug, message, exc_info)

    def warning(self, name, message, exc_info=False):
        """
        Log a warning-level message. If exc_info is True, if an exception
        was caught, show the exception information (message and stack trace).
        """
        logger = self.__get_logger(name)
        self._raw_log(logger.warning, message, exc_info)

    def error(self, name, message, exc_info=False):
        """
        Log an error-level message. If exc_info is True, if an exception
        was caught, show the exception information (message and stack trace).
        """
        logger = self.__get_logger(name)
        self._raw_log(logger.error, message, exc_info)
