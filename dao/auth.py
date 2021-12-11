import calendar
import datetime

from jwt import jwt


from dao.model.auth import Auth


class AuthDAO:
    def __init__(self, session, data, secret, algorithm):
        self.session = session
        self.data = data
        self.secret = secret
        self.algorithm = algorithm

    def create_token(self, data, secret, algorithm):
        return jwt.encode(data, secret, algorithm)

    def create_time_period1(self, minutes):
        time_period1 = datetime.datetime.utcnow() + datetime.timedelta(minutes)
        return time_period1

    def create_time_period2(self, days):
        time_period2 = datetime.datetime.utcnow() + datetime.timedelta(days)
        return time_period2

    def create_experation_date1(self, time_period1):
        exp_date = calendar.timegm(time_period1.timetuple())
        return exp_date

    def create_experation_date2(self, time_period2):
        exp_date = calendar.timegm(time_period2.timetuple())
        return exp_date