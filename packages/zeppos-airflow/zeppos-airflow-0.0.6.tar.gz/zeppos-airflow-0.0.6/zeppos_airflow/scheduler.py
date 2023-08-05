import pendulum
from datetime import datetime, timedelta

class Scheduler:
    class StartDate:
        @staticmethod
        def yesterday():
            now_utc = pendulum.now("utc")
            return now_utc.subtract(days=1, hours=now_utc.hour, minutes=now_utc.minute, seconds=now_utc.second,
                                    microseconds=now_utc.microsecond)

        @staticmethod
        def yesterday_usa_central_timezone():
            yesterday = pendulum.now("America/Chicago")
            return yesterday.subtract(days=1, hours=yesterday.hour, minutes=yesterday.minute, seconds=yesterday.second,
                                      microseconds=yesterday.microsecond)

        @staticmethod
        def one_hour_ago():
            now_utc = pendulum.now("utc")
            return now_utc.subtract(hours=1, minutes=now_utc.minute, seconds=now_utc.second,
                                    microseconds=now_utc.microsecond)

    class RetryDelay:
        @staticmethod
        def five_minutes():
            return timedelta(minutes=5)
