class DomainException(Exception):
    """Excepción base de dominio"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(DomainException):
    """Usuario ya existe"""
    def __init__(self, email: str):
        super().__init__(f"El usuario con email '{email}' ya existe")


class UserNotFoundException(DomainException):
    """Usuario no encontrado"""
    def __init__(self, identifier: str):
        super().__init__(f"Usuario '{identifier}' no encontrado")


class InvalidCredentialsException(DomainException):
    """Credenciales inválidas"""
    def __init__(self):
        super().__init__("Email o contraseña incorrectos")


class InactiveUserException(DomainException):
    """Usuario inactivo"""
    def __init__(self):
        super().__init__("Usuario inactivo. Contacta al administrador")


class InvalidTokenException(DomainException):
    """Token inválido o expirado"""
    def __init__(self):
        super().__init__("Token inválido o expirado")
