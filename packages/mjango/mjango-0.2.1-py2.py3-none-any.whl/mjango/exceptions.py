class DBError(Exception):
    pass


class QueryError(DBError):
    pass


class APIKeyError(DBError):
    pass


class ServiceError(DBError):
    pass


class SettingsError(DBError):
    pass


class InstanceNotFound(DBError):
    pass
