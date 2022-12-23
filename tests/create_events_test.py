import unittest
import io
import sys 
from unittest.mock import patch
from io import StringIO
import google_calendar_api

class MyTestCase(unittest.TestCase):

    suppress_text = io.StringIO()
    sys.stdout = suppress_text


    # @patch("sys.stdin", StringIO("1\n"))
    def test_event(self):
        service = google_calendar_api.authenticate_google()
        summary = "test"
        date = google_calendar_api.get_date("make a booking for next week friday ")

        result = google_calendar_api.create_event(service,summary, "CPT",date, date )
        self.assertTrue(result) 
        # self.assertNotEqual(result, 'volunteer')




if __name__ == "__main__":
    unittest.main()