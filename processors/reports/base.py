from dataloader.base import DataLoaderBase


class ReportBase(DataLoaderBase):

    def initialize(self):
        pass

    def execute(self):
        raise NotImplementedError()
