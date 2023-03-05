# Add Exceptions for New Player creation
class playerUserNameError(Exception):
    """Error raised when player name is less then 3 characters"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class playerMissingDataError(Exception):
    """Error raised when data is missing when trying to init a player"""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
    
class gameAttributesDataError(Exception):
    """Error raised when data is missing when trying to init a game attribute entity"""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)