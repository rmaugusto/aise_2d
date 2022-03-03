

from enum import Enum
from abc import ABC, abstractmethod


class ActivationFunction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def forward(self, inputs: list[float]) -> list[bool]:
        pass


class AiFunctionFactory:

    @staticmethod
    def create(function_name: str, input_count: int, hidden_layers_count: int, hidden_count: int,  output_count: int):
        if function_name == 'scratch_relu_01':
            from ai.scratch_relu_01 import ScratchReLU01
            return ScratchReLU01(input_count, hidden_layers_count, hidden_count, output_count)
        elif function_name == 'pytorch_relu_01':
            from ai.pytorch_relu_01 import PyTorchRelu01
            return PyTorchRelu01(input_count, hidden_layers_count, hidden_count, output_count)

        raise Exception('Unknown function')


class Brain:
    def __init__(self, function: ActivationFunction):
        self.function = function
        self.active = False
        self.id = None

    def forward(self, inputs: list[float]) -> list[float]:
        return self.function.forward(inputs)

    def copy_from(self, brain):
        pass


class AIMode(Enum):
    TRAINING = 'training'
    RUN = 'run'
    OFF = 'off'


class Ai:
    def __init__(self, function_name: str, ai_mode: AIMode, input_count: int, hidden_layers_count: int, hidden_count: int,  output_count: int):
        self.generation = 0
        self.function = AiFunctionFactory.create(
            function_name, input_count, hidden_layers_count, hidden_count, output_count)
        self.mode = ai_mode

    def has_learned_model(self):
        return False

    def start(self):

        if not self.has_learned_model() and self.mode == AIMode.RUN:
            raise Exception('No model has been learned')

        pass

    def begin_generation(self, brains: list[Brain]):
        self.generation += 1
        self.brains = brains

    def end_generation(self):
        self.brains = None

    def create_brain(self) -> Brain:
        return Brain(self.function)
