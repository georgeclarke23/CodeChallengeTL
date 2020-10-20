from sqlalchemy import create_engine
from app.config import Config


FINAL_DF = "final_df"


def write_dataframe(df_key):
    """Save the updated history to disk"""

    def write(config: Config):
        url = format_pyspark_jdbc_url(config)
        table = config.get("TABLE_NAME")
        config.info("WriteToPostgres", f"Writing dataframe to postgres {table}")

        engine = create_engine(url)
        config.get_dataframe(df_key).toPandas().to_sql(
            table, engine, index=False, if_exists="replace"
        )

        config.info("WriteToPostgres", f"Finished writing to postgres {table}")

    return write


def format_pyspark_jdbc_url(config: Config) -> str:
    """Format url as required by pyspark host"""
    return f'postgresql+psycopg2://{config.get("POSTGRESS_USERNAME")}:{config.get("POSTGRESS_PASSWORD")}@{config.get("POSTGRESS_HOST")}:5432/{config.get("POSTGRESS_DATABASE")}'
