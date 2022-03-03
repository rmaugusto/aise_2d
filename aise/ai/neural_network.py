"""Create classes representing neural networks and their components."""

from abc import abstractmethod
import random

class Neuron:
    def __init__(self):
        self.weights = []
        self.output = 0

    def randomize_weights(self):
        for i in range(len(self.weights)):
            self.weights[i] = random.random()

    @abstractmethod
    def create(neuron_count: int):
        n = Neuron()
        n.weights = [0] * neuron_count
        n.output = 0
        return n

class Layer:
    def __init__(self):
        self.neurons:list[Neuron] = []

    @abstractmethod
    def create(weight_count: int, neuron_count: int):
        l = Layer()
        l.neurons = [Neuron.create(neuron_count) for _ in range(weight_count)]
        return l

class NeuralNetwork:
    def __init__(self, input_count: int, hidden_layers_count: int, hidden_count: int,  output_count: int):
        self.input = Layer.create(input_count, input_count)
        self.hidden_layers = [Layer.create(hidden_count, hidden_count) for _ in range(hidden_layers_count)]
        self.output = Layer.create(output_count, output_count)

    def randomize_weights(self):
        for layer in self.hidden_layers:
            for neuron in layer.neurons:
                neuron.randomize_weights()