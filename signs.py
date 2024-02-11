from enum import Enum


class Sign(Enum):
    MINUS = '-'
    PLUS = '+'
    MULTIPLICATION = '*'
    DIVISION = '/'
    
    def __eq__(self, __value) -> bool:
        if isinstance(__value, str):
            return self.value == __value
        elif isinstance(__value, Sign):
            return self.value == __value.value
        return False


SIGNS = [Sign.MINUS.value, Sign.PLUS.value, Sign.MULTIPLICATION.value, Sign.DIVISION.value]
