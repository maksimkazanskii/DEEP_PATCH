from sklearn.model_selection import train_test_split
from torch.utils.data import Subset
import numpy as np
import csv
import cv2
import os
import torch

class DataSet():

    def __init__(self, config):
        image_folder = config['image_folder']
        label_file = config['label_file']

        label_dict = {}
        with open(label_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                label_dict[row['bam_name']] = row['age']
        print(label_dict)
        image_list = []
        label_list = []

        for _, dirs, _ in os.walk(image_folder):
            for dir in dirs:

                bam_folder = os.path.join(image_folder, dir)
                bam_images = []
                for filename in os.listdir(bam_folder):
                    img_path = os.path.join(bam_folder, filename)
                    img = cv2.imread(img_path)
                    img = img.reshape((3,20,20))
                    img = img / 255.0
                    if len(bam_images) == 0:
                        bam_images = [img]
                    else:
                        bam_images.append(img)
                bam_images = np.array(bam_images, dtype=np.float16)
                bam_images = np.expand_dims(bam_images,0)
                if len(image_list)==0:
                    image_list = np.copy(bam_images)
                else:
                    image_list = np.concatenate((image_list, bam_images))
                label_list.append((float)(label_dict[dir]))
        print(image_list)
        self.image_list = torch.from_numpy(image_list)  # torch.Tensor(image_list)
        self.label_list = torch.tensor(label_list)  # torch.Tensor(label_list)

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        image = self.image_list[idx]
        label = self.label_list[idx]
        sample = {"Image": image, "Label": label}
        return sample

    #def train_val_dataset(dataset, val_split=0.25):
    #    train_idx, val_idx = train_test_split(list(range(len(dataset))), test_size=val_split)
    #    datasets = {}
    #    datasets['train'] = Subset(dataset, train_idx)
    #    datasets['val'] = Subset(dataset, val_idx)
    #    return datasets