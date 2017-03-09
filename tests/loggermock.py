class LoggerMock(object):

    def __init__(self):
        self.msgs = []

    def log(self, msg):
        self.msgs.append(msg)

    def debug(self, msg):
        self.log(msg)

    def info(self, msg):
        self.log(msg)

    def warning(self, msg):
        print 'WARNING ' + msg
        self.log(msg)

    def error(self, msg):
        print 'ERROR ' + msg
        self.log(msg)
