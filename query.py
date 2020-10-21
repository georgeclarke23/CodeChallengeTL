from sqlalchemy import create_engine
import sys
import os
import pandas as pd


def main():
    if len(sys.argv) <= 0:
        print(f'{len(sys.argv)} {sys.argv[1]}')
        raise Exception(f"Need to provide a query")

    user = os.environ["POSTGRESS_USERNAME"]
    password = os.environ["POSTGRESS_PASSWORD"]
    host = os.environ["PGHOST"]
    db = os.environ["POSTGRESS_DATABASE"]

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db}")
    connection = engine.raw_connection()

    df = pd.read_sql(str(sys.argv[1]), connection)
    print(df.head())

    df.to_csv("results.csv")


if __name__ == "__main__":
    main()
