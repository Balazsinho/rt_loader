import os
import settings


class StopException(Exception):
    pass


class LoaderException(Exception):
    pass


class NotProcessableEmailError(Exception):
    pass


class ErrorsDuringProcess(Exception):
    pass


class LoaderBase(object):

    def __init__(self, logger):
        self.logger = logger
        self._duplicates = 0

    def _setup_env(self):
        if not os.path.exists(settings.EMAIL_SUCCESS_DIR):
            os.makedirs(settings.EMAIL_SUCCESS_DIR)

        if not os.path.exists(settings.EMAIL_ERROR_DIR):
            os.makedirs(settings.EMAIL_ERROR_DIR)

        if not os.path.exists(settings.EMAIL_NOTPROC_DIR):
            os.makedirs(settings.EMAIL_NOTPROC_DIR)

    def pre_run(self, args):
        self._setup_env()

    def run(self, args):
        raise NotImplementedError()

    # ========================================================================
    # Processing status forks
    # ========================================================================

    def _duplicate(self):
        self._duplicates += 1
        if self._duplicates > 70:
            raise StopException('Duplikaciok miatt leall')

    def _error(self, *args):
        pass

    def _success(self, *args):
        pass
