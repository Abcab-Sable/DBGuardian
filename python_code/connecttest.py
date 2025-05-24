import connect
import unittest
import pathlib
import os
import logging

def release_logging_handlers():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()

class TestLogPath(unittest.TestCase):

    def test_inc_log_path(self, inc_log_path="./test./log", cor_db_path="../db.db"):
        release_logging_handlers()
        error = False
        try:
            con = connect.connect_sqlite(cor_db_path, inc_log_path)
            con.close()

        except (FileNotFoundError, OSError, ValueError):
            error = True

        self.assertEqual(error, True, "A FileNotFoundError should be raised")

    def test_cor_log_path(self, cor_log_path="./test.log", cor_db_path="../db.db"):
        release_logging_handlers()
        error = False
        success = False
        log_path = pathlib.Path(cor_log_path)

        if log_path.exists():
            os.remove(log_path)
            
        try:
            con = connect.connect_sqlite(cor_db_path, cor_log_path)
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

        try:
            con = connect.connect_sqlite(inc_db_path, cor_log_path)
            con.close()
        except FileNotFoundError:
            error = True

        self.assertEqual(error, True, "A FileNotFoundError should occur")

if __name__ == "__main__":
    unittest.main()
