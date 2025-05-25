import connect
import unittest
import pathlib
import os
import logging

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


def release_logging_handlers():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()


class TestLogPath(unittest.TestCase):

    def test_inc_log_path(self, inc_log_path="./test./log", cor_db_path="../db.db"):
        release_logging_handlers()
        error = False
        try:
            con = connect.connect_sqlite(
                str(SCRIPT_DIR / cor_db_path), str(SCRIPT_DIR / inc_log_path)
            )
            con.close()

        except (FileNotFoundError, OSError, ValueError):
            error = True

        self.assertEqual(error, True, "A FileNotFoundError should be raised")

    def test_cor_log_path(self, cor_log_path="./test.log", cor_db_path="../db.db"):
        release_logging_handlers()
        error = False
        success = False
        log_path = SCRIPT_DIR / pathlib.Path(cor_log_path)

        if log_path.exists():
            os.remove(log_path)

        try:
            con = connect.connect_sqlite(
                str(SCRIPT_DIR / cor_db_path), str(SCRIPT_DIR / cor_log_path)
            )
            con.close()

        except:
            error = True

        if log_path.exists():
            success = True

        self.assertEqual(error, False, "No errors should occur")
        self.assertEqual(success, True, "Test log file should be created")


class TestDBPath(unittest.TestCase):

    def test_inc_db_path(self, cor_log_path="./test.log", inc_db_path="./db./db"):
        release_logging_handlers()
        error = False
        log = []
        expected_log = [
            "INFO:connect:STARTED\n",
            f"INFO:connect:log_path: {str(SCRIPT_DIR / cor_log_path)}\n",
            "ERROR:connect:FileNotFoundError\n",
            "INFO:connect:FINISHED\n",
        ]

        try:
            con = connect.connect_sqlite(
                str(SCRIPT_DIR / inc_db_path), str(SCRIPT_DIR / cor_log_path)
            )
            con.close()
        except FileNotFoundError:
            error = True

        with open(str(SCRIPT_DIR / cor_log_path), "r") as f:
            log = f.readlines()

        self.assertEqual(
            log,
            expected_log,
            "Log should start, log_path should be logged, FileNotFoundError should be logged, Log should finish",
        )
        self.assertEqual(error, True, "A FileNotFoundError should occur")

    def test_nexist_db_path(
        self, cor_log_path="./test.log", nexist_db_path="./nexist.db"
    ):
        release_logging_handlers()
        error = False
        log = []
        expected_log = [
            "INFO:connect:STARTED\n",
            f"INFO:connect:log_path: {str(SCRIPT_DIR / cor_log_path)}\n",
            "ERROR:connect:FileNotFoundError\n",
            "INFO:connect:FINISHED\n",
        ]

        try:
            con = connect.connect_sqlite(
                str(SCRIPT_DIR / nexist_db_path), str(SCRIPT_DIR / cor_log_path)
            )
            con.close()
        except FileNotFoundError:
            error = True

        with open(str(SCRIPT_DIR / cor_log_path), "r") as f:
            log = f.readlines()

        self.assertEqual(
            log,
            expected_log,
            "Log should start, log_path should be logged, FileNotFoundError should be logged, Log should finish",
        )
        self.assertEqual(error, True, "A FileNotFoundError should occur")


class TestSuccess(unittest.TestCase):

    def test_success(self, cor_db_path="../db.db", cor_log_path="./test.log"):
        log = []
        expected_log = [
            "INFO:connect:STARTED\n",
            f"INFO:connect:log_path: {str(SCRIPT_DIR / cor_log_path)}\n",
            f"INFO:connect:db_path: {str(SCRIPT_DIR / cor_db_path)}\n",
            f"INFO:connect:Successfully connected with {pathlib.Path(str(SCRIPT_DIR / cor_db_path)).name}\n",
            "INFO:connect:FINISHED\n"
        ]

        con = connect.connect_sqlite(
            str(SCRIPT_DIR / cor_db_path), str(SCRIPT_DIR / cor_log_path)
        )

        with open(str(SCRIPT_DIR / cor_log_path), "r") as f:
            log = f.readlines()

        self.assertEqual(log, expected_log, "Log Should: log start, log log_path, log db_path, log success, log finish")
        self.assertEqual(type(con).__name__, "Connection", "connect_sqlite should return a valid sqlite3 Connection object")

if __name__ == "__main__":
    unittest.main()
