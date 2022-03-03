
from ai.ai import ActivationFunction
from ai.neural_network import NeuralNetwork
class ScratchReLU01(ActivationFunction):

    BIAS = 1

    def __init__(self, input_count: int, hidden_layers_count: int, hidden_count: int,  output_count: int):
        super().__init__()

        # dtype = torch.float
        self.nn = NeuralNetwork(input_count, hidden_layers_count, hidden_count, output_count)

    def relu(self, x: float) -> float:
        if x < 0:
            return 0
        else:
            return 1

    def forward(self, inputs: list[float]) -> list[float]:
        
        for i in range(len(inputs) - ScratchReLU01.BIAS):
            self.nn.input.neurons[i].output = inputs[i]

        for i in range(len(self.nn.hidden_layers[0].neurons) - ScratchReLU01.BIAS):
            sum = 0
            for j in range(len(self.nn.input.neurons) - ScratchReLU01.BIAS):
                sum += self.nn.input.neurons[j].output * self.nn.hidden_layers[0].neurons[i].weights[j]

            self.nn.hidden_layers[0].neurons[i].output = self.relu(sum)

        for i in range(1, len(self.nn.hidden_layers)):
            for j in range(len(self.nn.hidden_layers[i].neurons) - ScratchReLU01.BIAS):
                sum = 0
                for k in range(len(self.nn.hidden_layers[i - 1].neurons) - ScratchReLU01.BIAS):
                    sum += self.nn.hidden_layers[i - 1].neurons[k].output * self.nn.hidden_layers[i].neurons[j].weights[k]

                self.nn.hidden_layers[i].neurons[j].output = self.relu(sum)

        last_hidden_layer = self.nn.hidden_layers[-1]
        for i in range(len(self.nn.output.neurons) - ScratchReLU01.BIAS):
            sum = 0
            for j in range(len(last_hidden_layer.neurons) - ScratchReLU01.BIAS):
                sum += last_hidden_layer.neurons[j].output * self.nn.output.neurons[i].weights[j]
            
            self.nn.output.neurons[i].output = self.relu(sum)

        return [n.output for n in self.nn.output.neurons]