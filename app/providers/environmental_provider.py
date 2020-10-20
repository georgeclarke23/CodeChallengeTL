import os


class EnvironmentVariablesProvider(object):
    def __init__(self, logging):
        self._logging = logging

    def get_var(self, key):
        if key not in ["LOG_LEVEL", "LOG_FORMAT"]:
            try:
                self._logging.debug(
                    "EnvironmentVariablesProvider",
                    f"Getting environment variable {key}",
                )
                return os.environ[key]
            except Exception:
                self._logging.error(
                    "EnvironmentVariablesProvider",
                    "Cannot find environment variable: {}".format(key),
                )
                raise EnvironmentError(f"Cannot find environment variable: {key}")

    def var_exists(self, key):
        if key not in ["LOG_LEVEL", "LOG_FORMAT"]:
            self._logging.debug(
                "EnvironmentVariablesProvider", f"Checking environment variable {key}"
            )
        return key in os.environ
