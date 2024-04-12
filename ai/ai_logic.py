from typing import List

import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim

# Define the model
class LSTMModel(nn.Module):
    def __init__(self, num_classes):
        super(LSTMModel, self).__init__()
        self.lstm1 = nn.LSTM(input_size=6, hidden_size=64, batch_first=True)
        self.dropout1 = nn.Dropout(0.5)
        self.lstm2 = nn.LSTM(input_size=64, hidden_size=32, batch_first=True)
        self.dropout2 = nn.Dropout(0.5)
        self.fc = nn.Linear(32, num_classes)

    def forward(self, x):
        # LSTM with input (batch, seq, feature) when batch_first=True
        x, _ = self.lstm1(x)  # output from first LSTM layer
        x = self.dropout1(x)
        x, _ = self.lstm2(x)  # output from second LSTM layer
        x = self.dropout2(x)
        x = x[:, -1, :]  # Select the last time step output for feeding into the fully connected layer
        out = self.fc(x)
        return out

def predict(model, sample):
    model.eval()
    sample_tensor = torch.tensor(sample, dtype=torch.float).unsqueeze(0)
    with torch.no_grad():
        sample_tensor = sample_tensor.to(device)
        output = model(sample_tensor)
        
        _, predicted_class = torch.max(output, dim=1)
        return predicted_class.item()
    

mappings ={'0': 'shield',
    '1': 'bomb',
    '2': 'hulk',
    '3': 'logout',
    '4': 'reload',
    '5': 'shangChi',
    '6': 'captAmerica',
    '7': 'ironMan',
    '8': 'nothing'}

device = torch.device("cpu")

class AILogic:
    def __init__(self):
        self.model = LSTMModel(num_classes=9)
        # self.model.load_state_dict(torch.load('/home/xilinx/external_comms/ai/lstm_model_94.pth'))
        self.model.load_state_dict(torch.load('/home/xilinx/external_comms/ai/lstm_with_nothing_state_v5.pth'))
        self.model.to(device)
        self.model.eval()

    def process(self, message: List[float]) -> str:
            sample = message
            final = [sample[i:i + 6] for i in range(0, len(sample), 6)]
            class_index = predict(self.model, final)
            # print(class_index)
            # print("Prediction is " + mappings[str(class_index)])
            action_name = mappings[str(class_index)]

            return action_name