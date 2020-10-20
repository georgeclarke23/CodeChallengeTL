from app.config import Config


def select_columns(df_name: str, columns: list):
    """Select Columns for dataFrame"""

    def select(config: Config):
        # Select columns from dataframe
        df = config.get_dataframe(df_name).select(*columns)

        # Store dataframe to config
        config.save_dataframe(df_name, df)

        config.info("SelectColumns", f"Selecting columns from Dataframe: {columns}")

    return select
