import pendulum


class Scheduler:
    class StartDate:
        @staticmethod
        def yesterday():
            yesterday = pendulum.now("America/Chicago")
            return yesterday.subtract(days=1, hours=yesterday.hour, minutes=yesterday.minute, seconds=yesterday.second,
                                      microseconds=yesterday.microsecond)
