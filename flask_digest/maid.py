
class Maid:
    def __init__(self):
        self.limit = 1

    def is_dirty(self, tokens):
        return len(tokens) > self.limit

    def clean(self, tokens):
        if self.is_dirty(tokens): self.purge(tokens)
        if self.is_dirty(tokens): self.limit *= 2

    def purge(self, tokens):
        for nonce, token in tokens.items():
            if token.stale():
                del tokens[nonce]
