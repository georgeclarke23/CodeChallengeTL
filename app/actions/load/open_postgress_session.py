from app.sessions.postgress_session import PostgressSession
from app.sessions.postgress_password_connection import PostgressPasswordConnection
from app.config import Config


def open_postgress_session_with_password(config: Config):
    """Opening a Postgres session and adding it to the Config"""
    if not config.session_exists("PostgresSession"):
        config.debug("PostgresSession", "Opening Postgres session using password")
        session = PostgressSession(config, PostgressPasswordConnection(config))
        config.add_session("PostgresSession", session)
        config.debug("PostgresSession", f"Postgres session added to sessions opened")
    else:
        config.debug("PostgresSession", f"Postgres session already exists")
