from pyspark.sql.functions import col, udf
from app.config import Config


def calculate_jaccard_score(df_key: str):
    def calculate(config: Config):
        df = config.get_dataframe(df_key)
        config.info("CalculateJaccardScore", f"Calculate priority process has started")

        df = df.withColumn(
            "jaccard_score",
            jaccard_similarity(col("year"), col("year_in_title"), col("type_in_title")),
        )

        # Store dataframe to config
        config.save_dataframe(df_key, df)

        config.info("CalculateJaccardScore", "Scores have been calculated.")

    return calculate


@udf
def jaccard_similarity(x1, y1, y2):
    intersection_cardinality = len(
        set.intersection(*[set([str(x1), "film"]), set([str(y1), str(y2)])])
    )
    union_cardinality = len(
        set.union(*[set([str(x1), "film"]), set([str(y1), str(y2)])])
    )
    return intersection_cardinality / float(union_cardinality)
