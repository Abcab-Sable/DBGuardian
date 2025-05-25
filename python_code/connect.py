# This is the python file, which sets up database connections

import sqlite3 # Usage of the sqlite3 library is required in order to connect to sqlite databases
import pathlib # pathlib is required in order to check if files and directories exist
import logging # logging is used to log important steps in the code execution, to provide a comprehensive review if something goes wrong
import os # os is used to remove files

logger = logging.getLogger(__name__) # logger object is used to actually log the steps

# This function takes parameters: db_path and log_path, which represent the database file path and the logging file path.
# The database file is required to exist beforehand, the logging file is not.
# First it validates the log_path to see if it is a valid path.
# Second it configures the logger, with a level of logging.INFO and logs the start of the function as well as the log_path
# Third it validates that the db_path exists, which also simulataneously checks that it is valid.
# Fourth it logs the db_path and attempts to establish a connection with the database.
# Fifth it either logs a success and finish and returns the connection or it fails, logs the specific error and logs finish.
def connect_sqlite(db_path, log_path="./connectpy.log"):
    with open(log_path, "w"): # this will raise an error if the log_path is invalid, which is picked up on by unit tests.
        pass

    logging.basicConfig(filename=log_path, level=logging.INFO) # this creates a basic logging configuration
    logger.info("STARTED")
    logger.info(f"log_path: {log_path}")
    try:
        db_path = pathlib.Path(db_path) # this converts db_path to a pathlib.Path object.
        if not db_path.exists():
            raise FileNotFoundError # a FileNotFoundError is raised if the db_path does not exist.
        logger.info(f"db_path: {db_path}")
        con = sqlite3.connect(db_path) # an attempt to connect to the database is made
        logger.info(f"Successfully connected with {db_path.name}")
        logger.info("FINISHED")
        return con # if successful, the connection to the database is returned

    except Exception as e:
        logger.error(f"{type(e).__name__}") # if an error occurs, it is logged
        logger.info("FINISHED")
        raise e


if __name__ == "__main__":
    connect_sqlite("../db./db", "./logging.logging") # simple manual test to see how the program handles invalid database paths
