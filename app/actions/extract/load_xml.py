from app.config import Config


def load_xml_file(path: str, row_tag: str, df_name: str):
    """Loading XML file to context"""

    def load_file(config: Config):
        spark = config.get_session("SparkSession")
        config.info("LoadXML", f"Loading {df_name} XML")
        df = (
            spark.read.format("com.databricks.spark.xml")
            .option("rowTag", row_tag)
            .load(path)
        )
        # Save dataframe to context
        config.save_dataframe(df_name, df)
        config.debug("LoadXML", f"Loaded {df_name} XML file")

    return load_file
