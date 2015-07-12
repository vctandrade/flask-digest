
class Maid(object):
    def __init__(self):
        self.limit = 1

    def __call__(self, tokens):
        if self.dirty(tokens): self.clean_up(tokens)
        if self.dirty(tokens): self.limit *= 2

    def dirty(self, tokens):
        return len(tokens) > self.limit

    def clean_up(self, tokens):
        for nonce, token in tokens.items():
            if token.stale(): del tokens[nonce]
