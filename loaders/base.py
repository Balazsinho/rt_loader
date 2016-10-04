class StopException(Exception):
    pass


class LoaderException(Exception):
    pass


class NotProcessableEmailError(Exception):
    pass


class LoaderBase(object):
    def __init__(self, logger):
        self.logger = logger
        self._duplicates = 0

    def pre_run(self, args):
        pass

    def run(self, args):
        raise NotImplementedError()

    def _duplicate(self):
        self._duplicates += 1
        if self._duplicates > 9:
            raise StopException('Duplikaciok miatt leall')
