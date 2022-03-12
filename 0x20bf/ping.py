from time_functions import btc_time, unix_time_millis


class Ping:
    def __init__(self, gpgr, gpgs):
        self.gpgr = gpgr
        self.gpgs = gpgs
        self.btc_time = btc_time()
        self.unix_time_millis = unix_time_millis()
        self.ping_data = [self.gpgr, self.gpgs, self.btc_time, self.unix_time_millis]
