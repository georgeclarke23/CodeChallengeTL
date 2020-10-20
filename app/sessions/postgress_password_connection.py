import psycopg2


class PostgressPasswordConnection(object):
    """ This class handle connecting to snowflake with username and password"""

    def __init__(self, config):
        self._config = config
        self._connectionDetails = {
            "user": self._config.get("POSTGRESS_USERNAME"),
            "password": self._config.get("POSTGRESS_PASSWORD"),
            "host": self._config.get("POSTGRESS_HOST"),
            "database": self._config.get("POSTGRESS_DATABASE"),
        }
        self.connection = None
        self.__open_connection()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def __open_connection(self):
        """
        Opens connection to Postgress
        :return: Postgress Connection
        """
        try:
            self._config.info(
                "PostgressPasswordConnection",
                "Connecting to Postgress with user:{user} on host:{host}".format(
                    **self._connectionDetails
                ),
            )
            self.connection = psycopg2.connect(**self._connectionDetails)
            self._config.info(
                "PostgressPasswordConnection",
                "Successfully connected to Postgress with user:{user} on host:{host}".format(
                    **self._connectionDetails
                ),
            )
        except Exception as e:
            self._config.error(
                "PostgressPasswordConnection", f"Error in connecting to Postgress: {e}"
            )
            raise

    def close(self):
        """Close Postgress connection"""
        if self.connection is not None and not self.connection.closed:
            self._config.debug(
                "PostgressPasswordConnection",
                "Closing connection to Postgress with user:{user} on host:{host}".format(
                    **self._connectionDetails
                ),
            )
            self.connection.close()
