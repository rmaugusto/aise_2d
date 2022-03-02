
from ai.ai import ActivationFunction


class ScratchReLU01(ActivationFunction):

    def __init__(self):
        super().__init__()

    def forward(self, inputs: list[float]):
        return inputs[0]
