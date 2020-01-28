
class Path(object):
    def __init__(self, bias, p, u):
        self.bias = bias
        self.abs_bias = abs(bias)
        self.p = p
        self.u = u
        self.u_idx = [block*len(ui)+offset for block, ui in u.items()
                      for offset in range(len(ui)) if (int(ui[offset]))]

    def __str__(self):
        return f"Bias: {self.bias}\nPlaintext bits: {self.p}\nLast round bits: {self.u}\nLast round indices: {self.u_idx}"
