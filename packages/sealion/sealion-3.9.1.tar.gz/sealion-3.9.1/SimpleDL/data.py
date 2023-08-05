'''
We'll feed inputs into our network in batches.
'''

from typing import Iterator, NamedTuple

from tensor import Tensor

import numpy as np

Batch = NamedTuple("Batch", [("inputs", Tensor), ("targets", Tensor)])

class DataIterator :
    def __call__(self, inputs : Tensor, targets : Tensor) -> Iterator[Batch]:
        raise NotImplementedError



class BatchIterator(DataIterator):
    def __init__(self, batch_size : int = 32, shuffle : bool = True) -> True:
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __call__(self, inputs: Tensor, targets: Tensor) -> Iterator[Batch]:
        starts = np.arange(0, len(inputs), self.batch_size)
        if self.shuffle :
            np.random.shuffle(starts)
        for start in starts :
            end = start + self.batch_size
            batch_inputs = inputs[start : end]
            batch_targets = targets[start : end]
            yield Batch(batch_inputs, batch_targets)



