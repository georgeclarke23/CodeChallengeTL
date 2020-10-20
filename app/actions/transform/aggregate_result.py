from app.config import Config


def aggregate_results(df_key: str):
    def agg(config: Config):
        df = config.get_dataframe(df_key)
        config.info("AggregateResults", "Aggregating results started")

        df = df.orderBy(["title", "jaccard_score"], ascending=False).drop_duplicates(
            subset=["title"]
        )

        # Store dataframe to config
        config.save_dataframe(df_key, df)

    return agg
