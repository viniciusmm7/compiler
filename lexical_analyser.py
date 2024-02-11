from re import findall


class LexicalAnalyser:
    def __init__(self, source_code: str):
        self.source_code: str = source_code

    def tokenize(self):
        tokens: list[str] = findall(r'\d+|\D', self.source_code)
        tokens = [token.strip() for token in tokens if token.strip()]
        return tokens
