class DocumentNotFound(Exception):
    pass


class PidNotFound(DocumentNotFound):
    pass


class IdNotFound(DocumentNotFound):
    pass
