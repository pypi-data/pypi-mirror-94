import os
from mjango import exceptions


class Settings:
    def __init__(self, db_host=None, db_name=None):
        self.db_host = db_host
        self.db_name = db_name


db_settings = Settings()
