class StamdataException(Exception):
    pass


class InvalidRelation(StamdataException):
    pass


class ResourceNotFound(StamdataException):
    pass


class InvalidField(StamdataException):
    pass
