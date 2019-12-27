from .model import Model
from ... import describe


@describe.attributes(
    nW=describe.Dimension("Number of surrounding tokens on each side to extract")
)
class ExtractWindow(Model):
    """Add context to vectors in a sequence by concatenating n surrounding
    vectors.

    If the input is (10, 32) and n=1, the output will be (10, 96), with
    output[i] made up of (input[i-1], input[i], input[i+1]).
    """

    name = "extract_window"

    def __init__(self, nW=1):
        Model.__init__(self)
        self.nW = nW

    def predict(self, X):
        return self.ops.seq2col(X, self.nW)

    def begin_update(self, X__bi):
        X__bo = self.ops.seq2col(X__bi, self.nW)
        
        def finish_update(gradient):
            return self.ops.backprop_seq2col(gradient, self.nW)
        
        return X__bo, finish_update
