import os
from typing import Optional
from mjango import exceptions


class Settings:
    def __init__(self,
                 db_host: Optional[str] = None,
                 db_name: Optional[str] = None) -> None:
        self.db_host = db_host
        self.db_name = db_name


db_settings = Settings()
