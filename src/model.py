import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):

    def __init__(self):
        super().__init__()
        self.first_layer = nn.Sequential(
            nn.Conv2d(in_channels = 3, out_channels= 32, kernel_size=3, padding=1),
            nn.ReLU()
        )
        self.second_layer = nn.Sequential(
            nn.Conv2d(in_channels= 32, out_channels= 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Flatten()
        )
        self.third_layer = nn.Sequential(
            nn.Linear(10 * 10 * 256, 256, bias = True),
            nn.ReLU(),
            nn.Linear(256, 4, bias = True)
        )
        """
        self.first_layer = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2),
            nn.Flatten()
        )

        self.second_layer = nn.Sequential(
            nn.Linear(in_features = 10 * 10 * 32, out_features = 128, bias=True),
            nn.ReLU(),
            nn.Linear(128, 1, bias=True)
        )
        """
        self.merge_net = nn.Sequential(
            nn.Linear(400, 64, bias = True),
            nn.ReLU(),
            nn.Linear(64, 1, bias = True)
        )

    def forward(self, x_tensor):
        batch_size      = x_tensor.size()[0]
        num_of_windows  = x_tensor.size()[1]
        num_of_channels = x_tensor.size()[2]
        window_size     = x_tensor.size()[3]
        x_tensor = x_tensor.view(num_of_windows, batch_size, num_of_channels, window_size, window_size)
        output_full = torch.tensor([])
        #print("PARAMS")
        #for param in self.parameters():
        #     print(param.data)
        #    break
        #print(x_tensor.size())
        for i, x  in enumerate(x_tensor):
            x = x.float()
            output = self.first_layer(x)
            output = self.second_layer(output)
            output = self.third_layer(output)
            output_full = torch.cat((output_full, output), 1)
        output_full = self.merge_net(output_full)
        output_full = output_full.view(1, batch_size)
        return output_full