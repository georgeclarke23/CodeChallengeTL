from app.config import Config
from app.sessions.spark_session import SparkSess


def open_spark_session(config: Config):
    """Opening a Spark session and adding it to the context"""
    if not config.session_exists("SparkSession"):
        config.debug("SparkSession", "Opening Spark session")
        session = SparkSess(config).spark
        config.add_session("SparkSession", session)
        config.debug("SparkSession", f"Spark session added to sessions opened")
    else:
        config.debug("SparkSession", f"Spark session already exists")
