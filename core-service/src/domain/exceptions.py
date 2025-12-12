# src/domain/exceptions.py
class DomainException(Exception):
    """Base exception for domain errors"""
    pass

class CattleNotFoundException(DomainException):
    pass

class RanchNotFoundException(DomainException):
    pass

class UnauthorizedAccessException(DomainException):
    pass

class DuplicateTagNumberException(DomainException):
    pass
