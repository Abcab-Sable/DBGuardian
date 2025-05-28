import connect
import unittest
import pathlib
import os
import logging
import sqlite3

from dotenv import load_dotenv
from typing import Type, Union

load_dotenv()
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
TEST_DB_PATH = SCRIPT_DIR / pathlib.Path(str(os.getenv("TEST_DATABASE_FILE_PATH")))
TEST_LOG_PATH = SCRIPT_DIR / pathlib.Path(str(os.getenv("TEST_LOG_FILE_PATH")))


def release_logging_handlers():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()


def check_path(
    db_path: Union[os.PathLike, str],
    log_path: Union[os.PathLike, str],
    errors_to_catch: list[Type[Exception]] = [Exception],
) -> tuple[Union[sqlite3.Connection, None], bool]:
    error: bool = False
    con: Union[sqlite3.Connection, None] = None

    try:
        con = connect.connect_sqlite(
            str(SCRIPT_DIR / db_path), str(SCRIPT_DIR / log_path)
        )

    except tuple([exception for exception in errors_to_catch]):
        error: bool = True

    return con, error


class TestLogPath(unittest.TestCase):

    def test_inc_log_path(self, inc_log_path="./test./log", cor_db_path=TEST_DB_PATH):
        release_logging_handlers()
        con, error = check_path(
            cor_db_path,
            inc_log_path,
            errors_to_catch=[FileNotFoundError, OSError, ValueError],
        )

        if con:
            con.close

        self.assertEqual(error, True, "A FileNotFoundError should be raised")

    def test_cor_log_path(self, cor_log_path=TEST_LOG_PATH, cor_db_path=TEST_DB_PATH):
        release_logging_handlers()
        error = False
        success = False
        log_path = SCRIPT_DIR / pathlib.Path(cor_log_path)

        if log_path.exists():
            os.remove(log_path)

        con, error = check_path(cor_db_path, cor_log_path)

        if con:
            con.close()

        success = log_path.exists()

        self.assertEqual(error, False, "No errors should occur")
        self.assertEqual(success, True, "Test log file should be created")


class TestDBPath(unittest.TestCase):

    def test_inc_db_path(self, cor_log_path=TEST_LOG_PATH, inc_db_path="./db./bp"):
        release_logging_handlers()
        error_occurs = False
        log = []
        expected_log = [
            f"INFO:connect:STARTED AT CWD: {os.getcwd()}\n",
            f"INFO:connect:log_path: {str(SCRIPT_DIR / cor_log_path)}\n",
            "INFO:connect:FINISHED\n",
        ]
        log_path = SCRIPT_DIR / pathlib.Path(cor_log_path)
        expected_error = "FileNotFoundError"

        if log_path.exists():
            os.remove(log_path)

        con, error_occurs = check_path(
            inc_db_path, cor_log_path, errors_to_catch=[FileNotFoundError]
        )

        if con:
            con.close()

        with open(str(SCRIPT_DIR / cor_log_path), "r") as f:
            log = f.readlines()
            actual_error = log[-2]
            log = log[0:2] + [log[-1]]

        self.assertEqual(
            log,
            expected_log,
            "Log should start, log_path should be logged, FileNotFoundError should be logged, Log should finish",
        )
        self.assertIn(
            expected_error,
            actual_error,
            "A FileNotFoundError stack trace should be logged",
        )
        self.assertEqual(error_occurs, True, "A FileNotFoundError should occur")

    def test_nexist_db_path(
        self, cor_log_path=TEST_LOG_PATH, nexist_db_path="./nexist.db"
    ):
        release_logging_handlers()
        log = []
        expected_log = [
            f"INFO:connect:STARTED AT CWD: {os.getcwd()}\n",
            f"INFO:connect:log_path: {str(SCRIPT_DIR / cor_log_path)}\n",
            "INFO:connect:FINISHED\n",
        ]
        expected_error = "FileNotFoundError"
        log_path = SCRIPT_DIR / pathlib.Path(cor_log_path)

        if log_path.exists():
            os.remove(log_path)

        con, error_occurs = check_path(
            nexist_db_path, cor_log_path, errors_to_catch=[FileNotFoundError]
        )

        if con:
            con.close()

        with open(str(SCRIPT_DIR / cor_log_path), "r") as f:
            log = f.readlines()
            actual_error = log[-2]
            log = log[0:2] + [log[-1]]

        self.assertEqual(
            log,
            expected_log,
            "Log should start, log_path should be logged, FileNotFoundError should be logged, Log should finish",
        )
        self.assertIn(
            expected_error,
            actual_error,
            "A FileNotFoundError stack trace should be logged",
        )
        self.assertEqual(error_occurs, True, "A FileNotFoundError should occur")


class TestSuccess(unittest.TestCase):

    def test_success(self, cor_db_path=TEST_DB_PATH, cor_log_path=TEST_LOG_PATH):
        log = []
        expected_log = [
            f"INFO:connect:STARTED AT CWD: {os.getcwd()}\n",
            f"INFO:connect:log_path: {str(SCRIPT_DIR / cor_log_path)}\n",
            f"INFO:connect:db_path: {str(SCRIPT_DIR / cor_db_path)}\n",
            f"INFO:connect:Successfully connected with {pathlib.Path(str(SCRIPT_DIR / cor_db_path)).name}\n",
            "INFO:connect:FINISHED\n",
        ]
        log_path = SCRIPT_DIR / pathlib.Path(cor_log_path)

        if log_path.exists():
            os.remove(log_path)

        con, error = check_path(cor_db_path, cor_log_path)

        with open(str(SCRIPT_DIR / cor_log_path), "r") as f:
            log = f.readlines()

        self.assertEqual(
            log,
            expected_log,
            "Log Should: log start, log log_path, log db_path, log success, log finish",
        )
        self.assertEqual(
            type(con).__name__,
            "Connection",
            "connect_sqlite should return a valid sqlite3 Connection object",
        )
        self.assertEqual(error, False, "No Error Should Occur")
        if con: con.close()


if __name__ == "__main__":
    # print(TEST_DB_PATH)
    # print(TEST_LOG_PATH)
    unittest.main()
