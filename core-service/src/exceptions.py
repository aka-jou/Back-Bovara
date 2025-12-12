class CattleNotFoundException(Exception):
    """Excepción cuando no se encuentra un animal"""
    def __init__(self, message: str = "Animal no encontrado"):
        self.message = message
        super().__init__(self.message)


class RanchNotFoundException(Exception):
    """Excepción cuando no se encuentra un rancho"""
    def __init__(self, message: str = "Rancho no encontrado"):
        self.message = message
        super().__init__(self.message)


class UnauthorizedAccessException(Exception):
    """Excepción cuando el usuario no tiene permisos"""
    def __init__(self, message: str = "No tienes permisos para acceder a este recurso"):
        self.message = message
        super().__init__(self.message)


class HealthEventNotFoundException(Exception):
    """Excepción cuando no se encuentra un evento de salud"""
    def __init__(self, message: str = "Evento de salud no encontrado"):
        self.message = message
        super().__init__(self.message)


class ReminderNotFoundException(Exception):
    """Excepción cuando no se encuentra un recordatorio"""
    def __init__(self, message: str = "Recordatorio no encontrado"):
        self.message = message
        super().__init__(self.message)
