from pyspark.sql.functions import broadcast, when, isnan, col
from app.config import Config


def join_df_on_key(
    key: list, df_names: list, final_df_name: str, columns: list, how: str = "left"
):
    """Inner joining two dataframes"""

    def join_df(config: Config):
        # Get dataframe from config
        dfs = config.get_dataframe()

        # Performing join
        count = 0
        df = dfs[df_names[count]]

        while (count + 1) < len(df_names):
            df = (
                df.alias("a")
                .join(
                    broadcast(dfs[df_names[count + 1]].alias("b")),
                    df[key[count][0]] == dfs[df_names[count + 1]][key[count][1]],
                    how=how,
                )
                .select(*columns[count])
            )

            count += 1

        # Store dataframe to config
        config.save_dataframe(final_df_name, df, clear=True)

        config.info("JoinDataframes", f"Joining Dataframe: {df_names}")

    return join_df
