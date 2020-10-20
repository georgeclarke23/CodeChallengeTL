# !/usr/bin/env python
# coding: utf-8

import os
from app.config import Config
from app.executors.executor import execute
from app.executors.loop_executor import loop_execute
from app.executors.retry_executor import retry_execute
from app.actions.load.close_sessions import close_sessions
from app.actions.load.open_spark_session import open_spark_session
from app.actions.extract.load_csv import load_csv_file
from app.actions.extract.load_xml import load_xml_file
from app.actions.transform.selecting_col_from_df import select_columns
from app.actions.transform.movies_etl import movies_etl
from app.actions.transform.joining_df_on_key import join_df_on_key
from app.actions.transform.ratings_etl import ratings_etl
from app.actions.transform.wiki_etl import wiki_etl
from app.actions.transform.calculate_score import calculate_jaccard_score
from app.actions.load.open_postgress_session import open_postgress_session_with_password
from app.actions.load.write_data_to_postgres import write_dataframe
from app.actions.transform.aggregate_result import aggregate_results

os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"

MOVIES_DF = "movies"
MOVIE_PATH = "datasets/movies/movies_metadata.csv"
MOVIE_COLUMNS = [
    "id",
    "original_title",
    "budget",
    "release_date",
    "revenue",
    "production_companies",
]
RATINGS_DF = "ratings"
RATINGS_PATH = "datasets/movies/ratings.csv"


MOVIE_RATINGS_DF = "MovieRatings"
MOVIE_RATINGS_MOVIE_COLUMNS = [
    "b.id",
    "b.title",
    "b.budget",
    "b.year",
    "b.revenue",
    "b.production_companies",
    "b.ratio",
    "a.rating",
]

WIKI_DF = "Wiki"
WIKI_PATH = "datasets/wiki/enwiki-latest-abstract.xml"
# WIKI_PATH = "datasets/wiki/test2.xml"
WIKI_ROW_TAG = "doc"

FINAL_DF = "final_df"
FINAL_DF_COLUMN = [
    "b.title",
    "b.budget",
    "b.year",
    "b.revenue",
    "b.ratio",
    "b.production_companies",
    "b.rating",
    "a.abstract",
    "a.url",
    "a.type_in_title",
    "a.year_in_title",
]


def main():
    # initialising Config
    config = Config()

    # adding actions to be executed
    actions = [
        # ETL actions
        retry_execute(open_postgress_session_with_password),
        execute(open_spark_session),
        execute(load_csv_file(MOVIE_PATH, MOVIES_DF)),
        execute(select_columns(MOVIES_DF, MOVIE_COLUMNS)),
        execute(movies_etl(MOVIES_DF)),
        execute(load_csv_file(RATINGS_PATH, RATINGS_DF)),
        execute(ratings_etl(RATINGS_DF)),
        execute(
            join_df_on_key(
                [["id", "id"]],
                [RATINGS_DF, MOVIES_DF],
                MOVIE_RATINGS_DF,
                [MOVIE_RATINGS_MOVIE_COLUMNS],
                "right",
            )
        ),
        execute(load_xml_file(WIKI_PATH, WIKI_ROW_TAG, WIKI_DF)),
        execute(wiki_etl(WIKI_DF)),
        execute(
            join_df_on_key(
                [["title", "title"]],
                [WIKI_DF, MOVIE_RATINGS_DF],
                FINAL_DF,
                [FINAL_DF_COLUMN],
                "right",
            )
        ),
        execute(calculate_jaccard_score(FINAL_DF)),
        execute(aggregate_results(FINAL_DF)),
        execute(write_dataframe(FINAL_DF)),
    ]

    # looping through actions and executing them
    execute_actions = loop_execute(actions)
    execute_actions(config)

    # closing and clearing all context sessions
    close_sessions(config)

    # Get dataframe from config
    config.info("Run", "Completed!!!!")


if __name__ == "__main__":
    main()
