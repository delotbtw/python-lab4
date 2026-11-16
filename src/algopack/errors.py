class AlgoError(Exception):
    """Base error of package"""


class InvalidInputError(AlgoError):
    def __init__(self, message: str) -> None:
        """Bad argument value or type"""
        self.message = message
        super().__init__(message)


class EmptyStructureError(AlgoError):
    def __init__(self, operation: str) -> None:
        """Operation on empty structure"""
        self.operation = operation
        super().__init__(f"{operation} on empty structure")
