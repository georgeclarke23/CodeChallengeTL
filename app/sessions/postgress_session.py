class PostgressSession(object):
    """This class creates a session with Postgress, where the Postgress cursor is used to execute queries"""

    def __init__(self, context, connection):
        self._context = context
        self.connection = connection
        self.__open_cursor()

    def __del__(self):
        return self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def __open_cursor(self):
        """Open the cursor and setting up postgress to execute queries"""
        try:
            self._context.info(
                "PostgressSession",
                "Initialising session cursor for postgress connection",
            )
            self.cursor = self.connection.connection.cursor()
            self._context.info(
                "PostgressSession",
                "Successfully initialised session cursor for postgress",
            )

            self._context.info(
                "PostgressSession",
                f"{self.connection.connection.get_dsn_parameters()}",
            )
            # Print PostgreSQL version
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()

            self._context.info(
                "PostgressSession",
                f"You are connected to - {record}",
            )
            return self.cursor
        except Exception as e:
            self._context.error(
                "PostgressSession", f"Error in initialising session cursor: {e}"
            )
            raise

    def close(self):
        """Closing the cursor from Postgress"""
        if self.cursor is not None and not self.cursor.closed:
            self._context.debug(
                "PostgressSession", "Closing session cursor for postgress:"
            )
            self.cursor.close()
