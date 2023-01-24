import numpy as np
import torch
from torch_geometric.nn import to_hetero, SAGEConv
from torch.nn import Linear, Dropout
import random




class GNNEncoder(torch.nn.Module):

    def __init__(self, hidden_channels, out_channels, p=0.2):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels, aggr='sum')
        self.conv2 = SAGEConv((-1, -1), out_channels, aggr='sum')
        self.dropout = Dropout(p)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        return x



class EdgeClassifier(torch.nn.Module):

    def __init__(self, hidden_channels):
        super().__init__()
        self.lin1 = Linear(2 * hidden_channels, hidden_channels)
        self.lin2 = Linear(hidden_channels, 1)
    
    def forward(self, z_dict, edge_label_index):
        row, col = edge_label_index
        z = torch.cat([z_dict['drug'][row], z_dict['protein'][col]], dim=-1)
        z = self.lin1(z).relu()
        z = self.lin2(z)
        return z.view(-1)


class Model(torch.nn.Module):

    def __init__(self, hidden_channels, data):
        super().__init__()
        self.encoder = GNNEncoder(hidden_channels, hidden_channels)
        self.encoder = to_hetero(self.encoder, data.metadata(), aggr='sum')
        self.decoder = EdgeClassifier(hidden_channels)
    
    def forward(self, x_dict, edge_index_dict, edge_label_index):
        z_dict = self.encoder(x_dict, edge_index_dict)
        out = self.decoder(z_dict, edge_label_index)
        return z_dict, out




class EarlyStopper():
    def __init__(self, tolerance=5, min_delta=0):

        self.tolerance = tolerance
        self.min_delta = min_delta
        self.counter = 0

    def early_stop(self, train_loss, validation_loss):
        if (validation_loss - train_loss) > self.min_delta:
            self.counter +=1
            if self.counter >= self.tolerance:  
                return True
        return False




def shuffle_label_data(train_data, a = ('drug', 'interaction', 'protein') ):
    
    length = train_data[a].edge_label.shape[0]
    lff = list(np.arange(length))
    random.shuffle(lff)

    train_data[a].edge_label = train_data[a].edge_label[lff]
    train_data[a].edge_label_index =  train_data[a].edge_label_index[:, lff]
    return train_data