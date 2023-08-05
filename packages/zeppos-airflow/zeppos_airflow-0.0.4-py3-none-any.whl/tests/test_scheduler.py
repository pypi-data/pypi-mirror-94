import unittest
from zeppos_airflow.scheduler import Scheduler
from datetime import datetime, timedelta

class TestTheProjectMethods(unittest.TestCase):
    def test_yesterday_methods(self):
        now = datetime.now() - timedelta(days=1)
        self.assertEqual(now.year, Scheduler.StartDate.yesterday().year)
        self.assertEqual(now.month , Scheduler.StartDate.yesterday().month)
        self.assertEqual(now.day, Scheduler.StartDate.yesterday().day)
        self.assertEqual(0, Scheduler.StartDate.yesterday().hour)
        self.assertEqual(0, Scheduler.StartDate.yesterday().minute)
        self.assertEqual(0, Scheduler.StartDate.yesterday().second)
        self.assertEqual(0, Scheduler.StartDate.yesterday().microsecond)


if __name__ == '__main__':
    unittest.main()
