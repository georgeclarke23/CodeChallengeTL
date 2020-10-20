from pyspark.sql import SparkSession
from pyspark import SparkConf


class SparkSess(object):
    def __init__(self, config):
        self._config = config
        self.spark = None
        self.__open_spark_session()

    def __open_spark_session(self):
        """Opening a Spark session"""
        self.spark = (
            SparkSession.builder.master(self._config.get("MASTER_NODE"))
            .config(conf=self.get_conf())
            .getOrCreate()
        )
        return self.spark

    def get_conf(self, parallellism: int = 2):
        """Get a config that is suitable for local development"""
        conf = (
            SparkConf()
            .setAppName(self._config.get("APP_NAME"))
            .set("spark.sql.session.timeZone", "UTC")
        )
        conf.set("spark.sql.shuffle.partitions", parallellism)
        conf.set("spark.default.parallelism", parallellism)
        conf.set("spark.sql.sources.partitionColumnTypeInference.enabled", "true")
        conf.set("spark.driver.host", "localhost")
        conf.setMaster("local[*]")
        conf.set("spark.executorEnv.PYTHONHASHSEED", 0)
        conf.set("spark.driver.memory", "2G")
        conf.set("spark.jars", "jars/spark-xml_2.12-0.10.0.jar")
        return conf
