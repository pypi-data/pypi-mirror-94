import os
from mjango import exceptions


class Settings:
    def __init__(self, db_host=None, db_name=None):
        self.db_host = None
        self.db_name = None


db_settings = Settings()
