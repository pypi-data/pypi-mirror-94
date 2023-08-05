import unittest
from zeppos_airflow.scheduler import Scheduler
from datetime import datetime, timedelta

class TestTheProjectMethods(unittest.TestCase):
    def test_startdate_yesterday_method(self):
        now = datetime.utcnow() - timedelta(days=1)
        self.assertEqual(now.year, Scheduler.StartDate.yesterday().year)
        self.assertEqual(now.month , Scheduler.StartDate.yesterday().month)
        self.assertEqual(now.day, Scheduler.StartDate.yesterday().day)
        self.assertEqual(0, Scheduler.StartDate.yesterday().hour)
        self.assertEqual(0, Scheduler.StartDate.yesterday().minute)
        self.assertEqual(0, Scheduler.StartDate.yesterday().second)
        self.assertEqual(0, Scheduler.StartDate.yesterday().microsecond)

    def test_startdate_yesterday_usa_central_timezone_method(self):
        # This test works if you are on US Central time zone.
        # TODO: Make timezone sensative.
        now = datetime.now() - timedelta(days=1)
        self.assertEqual(now.year, Scheduler.StartDate.yesterday_usa_central_timezone().year)
        self.assertEqual(now.month , Scheduler.StartDate.yesterday_usa_central_timezone().month)
        self.assertEqual(now.day, Scheduler.StartDate.yesterday_usa_central_timezone().day)
        self.assertEqual(0, Scheduler.StartDate.yesterday_usa_central_timezone().hour)
        self.assertEqual(0, Scheduler.StartDate.yesterday_usa_central_timezone().minute)
        self.assertEqual(0, Scheduler.StartDate.yesterday_usa_central_timezone().second)
        self.assertEqual(0, Scheduler.StartDate.yesterday_usa_central_timezone().microsecond)

    def test_retry_delay_five_minutes_method(self):
        self.assertEqual('0:05:00', str(Scheduler.RetryDelay.five_minutes()))


if __name__ == '__main__':
    unittest.main()
