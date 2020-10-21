from pyspark.sql.functions import trim, col, when, regexp_extract, round
from pyspark.sql.types import DoubleType, IntegerType
from app.config import Config


def movies_etl(df_name: str):
    """Performing ETL on the Movies Dataframe"""

    def etl(config: Config):
        # Get dataframe from config
        df = config.get_dataframe(df_name)

        config.info("MoviesETL", f"Movies dataframe ETL Started")
        df = (
            df.withColumn(
                "id",
                when(col("id").rlike(r"[\d]+"), col("id"))
                .otherwise(None)
                .cast(IntegerType()),
            )
            .withColumn(
                "revenue",
                when(col("revenue").rlike(r"[\d]+"), col("revenue"))
                .otherwise(0)
                .cast(DoubleType()),
            )
            .withColumn(
                "budget",
                when(col("budget").rlike(r"[\d]+"), col("budget"))
                .otherwise(0)
                .cast(DoubleType()),
            )
            .withColumn(
                "ratio",
                round((col("budget") / col("revenue")), 2),
            )
            .withColumn(
                "year",
                trim(regexp_extract(col("release_date"), r"([\d]{4})\-", 1)).cast(
                    IntegerType()
                ),
            )
            .withColumn("title", trim(col("original_title")))
            .orderBy(col("ratio").desc())
            .drop_duplicates(subset=["id"])
        )
        config.info("MoviesETL", f"Schema: ")
        df.printSchema()

        # Store dataframe to config
        config.save_dataframe(df_name, df)

        config.info("MoviesETL", f"Movies dataframe ETL Done")

    return etl
