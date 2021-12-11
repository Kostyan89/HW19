import calendar
import datetime

from jwt import jwt

from dao.model import Auth
from dao.model.auth import Auth


class AuthDAO:
    def __init__(self, session, data, secret, algorithm):
        self.session = session
        self.data = data
        self.secret = secret
        self.algorithm = algorithm

    def create_token(self, data, secret, algorithm, minutes:int, days:int):
        return jwt.encode(data, secret, algorithm)

    def create_time_period(self, data, time):
        time_period = datetime.datetime.utcnow() + datetime.timedelta(time)
        return time_period

    def create_experation_date(self, time_period):
        return calendar.timegm(time_period.timetuple())