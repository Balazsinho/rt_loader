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

    def __init__(self, logger, args):
        self.logger = logger
        self._duplicates = 0
        self._args = args

    def _setup_env(self):
        if not os.path.exists(settings.EMAIL_SUCCESS_DIR):
            os.makedirs(settings.EMAIL_SUCCESS_DIR)

        if not os.path.exists(settings.EMAIL_ERROR_DIR):
            os.makedirs(settings.EMAIL_ERROR_DIR)

        if not os.path.exists(settings.EMAIL_NOTPROC_DIR):
            os.makedirs(settings.EMAIL_NOTPROC_DIR)

    def pre_run(self):
        self._setup_env()

    def run(self):
        raise NotImplementedError()

    # ========================================================================
    # Processing status forks
    # ========================================================================

    def _duplicate(self, *args):
        self._duplicates += 1
        if self._duplicates > self._args.duplicates:
            raise StopException('Duplikaciok miatt leall')

    def _error(self, *args):
        pass

    def _notproc(self, *args):
        pass

    def _success(self, *args):
        self._duplicates = 0
