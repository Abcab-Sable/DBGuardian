# This is the python file, which sets up database connections

import sqlite3
import pathlib
import logging

logger = logging.getLogger(__name__)


def connect_sqlite(db_path, log_path="./connectpy.log"):
    try:
        with open(log_path, "w") as temp_file:
            pass

    except Exception as e:
        raise e

    logging.basicConfig(filename=log_path, level=logging.INFO)
    logger.info("STARTED")
    logger.info(f"log_path: {log_path}")
    try:
        logger.info(f"db_path: {db_path}")
        db_path = pathlib.Path(db_path)
        if not db_path.exists():
            raise FileNotFoundError
        con = sqlite3.connect(db_path)
        logger.info(f"Successfully connected with {db_path}")
        logger.info("FINISHED")
        return con

    except Exception as e:
        logger.error(f"{e}")
        logger.info("FINISHED")
        raise e


if __name__ == "__main__":
    connect_sqlite("../db.db", "./logging.logging./logging")
