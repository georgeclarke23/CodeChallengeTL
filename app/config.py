import copy
from app.providers.logging_provider import LoggingProvider
from app.providers.environmental_provider import EnvironmentVariablesProvider


class Config:
    def __init__(self, logger=None, env_vars=None):
        self._logger = LoggingProvider() if logger is None else logger
        self._env_vars = (
            EnvironmentVariablesProvider(self._logger) if env_vars is None else env_vars
        )
        self.state = {"df": {}}
        self.sessions = {}
        self.history = []
        self.is_error = False
        self.errors = []

    def info(self, name, message, exc_info=False):
        self._logger.info(name, message, exc_info)

    def debug(self, name, message, exc_info=False):
        self._logger.debug(name, message, exc_info)

    def warning(self, name, message, exc_info=False):
        self._logger.warning(name, message, exc_info)

    def error(self, name, message, exc_info=False):
        self._logger.error(name, message, exc_info)

    # Special functions for action retrying
    def snapshot_state(self):
        self.history.append(copy.deepcopy(self.state))

    def rollback_state(self):
        self.state = self.history.pop()
        self.clear_errors()

    def get(self, *args):
        if len(args) == 0:
            return self.state
        if len(args) == 1:
            if not isinstance(args[0], str):
                raise ValueError(
                    "Context variables can only be retrieved via a string key, argument is not a string"
                )
            return self.__get_var(args[0])
        else:
            vars = []
            for var in args:
                if not isinstance(var, str):
                    raise ValueError(
                        "Context variables can only be retrieved via a string key, argument is not a string"
                    )
                vars.append(self.__get_var(var))
            return vars

    def set(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            raise ValueError(
                "Setting variables onto the state requires named arguments or a dictionary"
            )
        for arg in args:
            if not isinstance(arg, dict):
                raise ValueError(
                    "Setting variables onto the state does not support non dictionary or non-named arguments"
                )
            self.state.update(arg)
        if len(kwargs) > 0:
            self.state.update(kwargs)

    def __get_var(self, key):
        if key in self.state:
            return self.state[key]
        else:
            return self._env_vars.get_var(key)

    def var_exists(self, key):
        if key in self.state:
            return True
        else:
            return self._env_vars.var_exists(key)

    def get_if_exists(self, key, default=None):
        if self.var_exists(key):
            return self.get(key)
        return default

    def add_session(self, name, shared):
        if name in self.sessions:
            raise KeyError("Session already exists on state")
        self.sessions[name] = shared

    def get_session(self, name):
        if name not in self.sessions:
            raise KeyError("Session has not been initialized on state")
        return self.sessions[name]

    def session_exists(self, name):
        return name in self.sessions

    def close_sessions(self):
        for name in self.sessions:
            if name != "SparkSession":
                self.sessions[name].close()
        self.sessions.clear()

    def close_session(self, name):
        self.sessions[name].close()
        del self.sessions[name]

    def set_error(self, error):
        self.is_error = True
        self.errors.append(error)

    def clear_errors(self):
        self.is_error = False
        self.errors.clear()

    def get_dataframe(self, df_key=None):
        if df_key is None:
            return self.state["df"]
        return self.state["df"][df_key]

    def save_dataframe(self, df_key, df, clear=False):
        if clear:
            self.state["df"].clear()
        self.state["df"][df_key] = df
