import torch
import torch.nn as nn


class FFN(nn.Module):    
    def __init__(self, n_input, n_output, n_hidden=3, hidden_dim=16):
        super().__init__()
        self.n_input = n_input
        self.n_output = n_output
        self.n_hidden = n_hidden
        self.hidden_dim = hidden_dim
        
        layers = [nn.Linear(n_input, hidden_dim)]
        layers.extend([nn.Linear(hidden_dim, hidden_dim) for _ in range(n_hidden - 1)])
        layers.append(nn.Linear(hidden_dim, n_output))
        self.model = nn.Sequential(*layers)
        
    def name(self):
        return f"{self.n_input}_{self.n_output}_{self.n_hidden}_{self.hidden_dim}"
    
    def forward(self, x):
        output = self.model(x)
        return output / output.norm()