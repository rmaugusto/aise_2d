
import numpy as np
from ai.ai import ActivationFunction
import torch
from torch import nn
from torch import optim


class PyTorchRelu01(ActivationFunction):

    def __init__(self, input_count: int, hidden_layers_count: int, hidden_count: int,  output_count: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_count, hidden_count),
            nn.ReLU(),
            nn.Linear(hidden_count, hidden_count),
            nn.ReLU(),
            nn.Linear(hidden_count, output_count),
        )

        self.optimizer = optim.Adam(self.network.parameters(), lr=0.01)
        self.loss_func = nn.MSELoss()

    def forward(self, inputs: list[float]) -> list[bool]:
        self.optimizer.zero_grad()
        output = self.network(torch.Tensor(np.array(inputs)))
        loss = self.loss_func(output, torch.Tensor(np.array(inputs)))
        loss.backward()
        self.optimizer.step()

        # actions = self.network(torch.Tensor(np.array(inputs))).tolist()
        # return [True if x > 0 else False for x in actions]
