from pyspark.sql.functions import split, trim, regexp_extract, col, when
from pyspark.sql import functions as F
from app.config import Config


def wiki_etl(df_key: str):
    """Performing ETL on the Movies Dataframe"""

    def etl(config: Config):
        # Get dataframe from config
        df = config.get_dataframe(df_key)

        config.info("WikiETL", "Wiki dataframe ETL started")

        df = (
            df.drop("links")
            .withColumn(
                "year_in_title",
                when(
                    col("title").rlike(".*\([\d]{4}[^\)]*\)$"),
                    trim(regexp_extract(col("title"), ".*\(([\d]{4})[^\)]*\)$", 1)),
                ).otherwise(None),
            )
            .withColumn(
                "type_in_title",
                when(
                    col("title").rlike(".*\(([\d]{4})?[^\)]*\)$"),
                    trim(
                        regexp_extract(
                            col("title"), ".*\(([\d]{4}[\s]+|)([^\)]*)\)$", 2
                        )
                    ),
                ).otherwise(None),
            )
            .withColumn(
                "title",
                trim(regexp_extract(col("title"), "([^:]+):([^(]+)(.*)", 2)),
            )
        )

        # Store dataframe to config
        config.save_dataframe(df_key, df)
        config.info("WikiETL", "Wiki dataframe ETL Done")

    return etl
