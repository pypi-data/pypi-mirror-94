# pyopenset

Pyopenset is a package that implements the meyhodology described in the paper:

It allows a easy and intuitive way to add novel classes to a pretrained model without requiring further optimization, New classes will always be added after the last.

So for example if your model has 10 neurons each for a single class ,the new class would be associated with neuron 11.

Note that current implementation only supports softmax activation functions on the last layer.
