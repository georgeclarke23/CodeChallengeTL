from pyspark.sql.functions import trim, col, when, mean, round
from pyspark.sql.types import IntegerType
from app.config import Config


def ratings_etl(df_name: str):
    """Performing ETL on the Movies Dataframe"""

    def etl(config: Config):
        # Get dataframe from config
        df = config.get_dataframe(df_name)

        config.info("RatingsETL", f"Ratings dataframe ETL Starterd")

        # Performing an aggregation on the ratings
        df = (
            df.withColumn(
                "id",
                when(col("movieId").rlike(r"[\d]+"), col("movieId"))
                .otherwise(None)
                .cast(IntegerType()),
            )
            .groupBy("id")
            .agg(round(mean("rating"), 2).alias("rating"))
        )

        # Store dataframe to config
        config.save_dataframe(df_name, df)

        config.info("RatingsETL", f"Ratings dataframe ETL Done")
        config.info("RatingsETL", f"Schema: ")
        df.printSchema()

    return etl
