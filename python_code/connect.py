# This is the python file, which sets up database connections

from dotenv import load_dotenv
import sqlite3 # Usage of the sqlite3 library is required in order to connect to sqlite databases
import pathlib # pathlib is required in order to check if files and directories exist
import logging # logging is used to log important steps in the code execution, to provide a comprehensive review if something goes wrong
import os

logger = logging.getLogger(__name__) # logger object is used to actually log the steps
load_dotenv()
LOG_PATH = os.getenv("CONNECTPY_LOG_FILE_PATH")
CWD = os.getcwd()

def validate_path_existence(path):
    path = pathlib.Path(path)
    if not path.exists():
        raise FileNotFoundError
    
    return path

def setup_logger(log_path=LOG_PATH):
    logging.basicConfig(filename=log_path, level=logging.INFO)

# This function takes parameters: db_path and log_path, which represent the database file path and the logging file path.
# The database file is required to exist beforehand, the logging file is not.
# First it validates the log_path to see if it is a valid path.
# Second it configures the logger, with a level of logging.INFO and logs the start of the function as well as the log_path
# Third it validates that the db_path exists, which also simulataneously checks that it is valid.
# Fourth it logs the db_path and attempts to establish a connection with the database.
# Fifth it either logs a success and finish and returns the connection or it fails, logs the specific error and logs finish.
def connect_sqlite(db_path, log_path=LOG_PATH):

    setup_logger(log_path)
    logger.info(f"STARTED AT CWD: {CWD}")
    logger.info(f"log_path: {log_path}")

    try:
        db_path = validate_path_existence(db_path)
        logger.info(f"db_path: {db_path}")
        con = sqlite3.connect(db_path) # an attempt to connect to the database is made
        logger.info(f"Successfully connected with {db_path.name}")
        logger.info("FINISHED")
        return con # if successful, the connection to the database is returned

    except (FileNotFoundError, PermissionError, OSError, sqlite3.OperationalError, sqlite3.DatabaseError, IOError, ValueError, sqlite3.Error) as e:
        logger.exception(e) # if an error occurs, it is logged
        logger.info("FINISHED")
        raise e


if __name__ == "__main__":
    #connect_sqlite("./db.db") # simple manual test to see how the program handles invalid database paths
    pass