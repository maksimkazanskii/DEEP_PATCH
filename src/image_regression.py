import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from model import Net
from dataloader import *
from torch import optim
import random
from logger import logger

CONFIG = {
    'num_epochs': 100,
    'batch_size': 32,
    'val_split_ratio': 0.67,
    'PATH_MODELS':"../experiments/",
    'EXP_NAME': "example_classification",
    'image_folder': "../../images_clean",
    'label_file'  : "../../labels/labels.csv",
    'lr' : 0.0001,
    'logging': True,
    'folder': "../experiments/exp_35files"
    }

if __name__ == '__main__':
    np.random.seed(37)
    torch.manual_seed(37)
    random.seed(37)

    logger = logger(CONFIG)
    logger.create_experiment()

    dataset = DataSet(CONFIG)
    (train_dataset, val_dataset) = train_test_split(dataset, train_size=CONFIG['val_split_ratio'])
    train_loader = DataLoader(train_dataset, batch_size=CONFIG['batch_size'], shuffle=True, num_workers = 0)
    val_loader = DataLoader(val_dataset, batch_size=CONFIG['batch_size'], shuffle=False, num_workers = 0)

    net = Net()
    loss_MAE = nn.L1Loss()
    optimizer = optim.Adam(net.parameters(), lr=CONFIG['lr'])
    experiment_folder = os.path.join(CONFIG['PATH_MODELS'], CONFIG['EXP_NAME'])

    for epoch in range(CONFIG['num_epochs']):  # loop over the dataset multiple times
        train_step  = 0
        train_loss = 0.0
        train_deviation = torch.Tensor([])
        for i, data in enumerate(train_loader, 0):
            inputs = data['Image']
            labels = data['Label']
            labels = labels[None, :]/10000
            optimizer.zero_grad()
            outputs = net(inputs)
            #print(labels, outputs)
            loss = loss_MAE(outputs, labels)
            #print(loss)

            loss.backward()
            #print("BACKWORDS)")
            optimizer.step()
            train_loss += loss.item()
            train_deviation = torch.cat((train_deviation, torch.abs(outputs - labels)))
            train_step += labels.size(dim=1)

        val_step = 0
        val_loss = 0.0
        val_deviation = torch.Tensor([])
        for i, data in enumerate(val_loader, 0):
            inputs = data['Image']
            labels = data['Label']
            labels = labels[None, :]/10000
            outputs = net(inputs)
            loss = loss_MAE(outputs, labels)
            val_loss += loss.item()
            val_deviation = torch.cat((val_deviation, torch.abs(outputs - labels)))
            val_step += labels.size(dim=1)
        #torch.save({
        #    'epoch': epoch,
        #    'model_state_dict': net.state_dict(),
        #    'optimizer_state_dict': optimizer.state_dict(),
        #    'val_loss': val_loss,
        #    'train_loss':train_loss
        #    }, experiment_folder, CONFIG['EXP_NAME'])
        #print(train_deviation,train_step)
        train_deviation = train_deviation.sum()/train_step
        loss_train_aver = train_loss / train_step
        val_deviation   = val_deviation.sum() / val_step
        loss_val_aver   = val_loss/train_step
        print("Epoch: ", epoch, "training loss: ",loss_train_aver,
              "validation loss:", val_loss/val_step/ CONFIG['batch_size'],
              "Train deviation:", train_deviation.item() ," Val  deviation: ", val_deviation.item() )
        logger.log([epoch, loss_train_aver, loss_val_aver, train_deviation.item(),
                    val_deviation.item()])
        logger.create_report()
    print('Finished Training')