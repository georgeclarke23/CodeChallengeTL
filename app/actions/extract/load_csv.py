from app.config import Config


def load_csv_file(path: str, df_name: str):
    """Loading XML file to context"""

    def load_file(config: Config):
        spark = config.get_session("SparkSession")
        config.info("LoadCSV", f"Loading {df_name} CSV file")
        df = spark.read.csv(
            path=path, header=True, inferSchema=True, quote='"', escape='"'
        )
        config.save_dataframe(df_name, df)
        config.info("LoadCSV", f"Loaded {df_name} CSV file")

    return load_file
