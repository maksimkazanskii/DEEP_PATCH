from datetime import datetime
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

class logger():

    def __init__(self, debug_conf):
        self.debug_conf = debug_conf

    def create_experiment(self, folder_name=False):
        if self.debug_conf['logging']==True:
            print("Logging is enabled ...")
            parent_dir = self.debug_conf['folder']
            if folder_name==False:
                now = datetime.now()
                name = now.strftime("%m_%d_%Y_%Hh%Mm%Ss")
            else:
                name = folder_name
            path = os.path.join(parent_dir, name)
            self.path_folder = path
            self.path_folder_images = os.path.join(path, "images")
            print("Creating an experiment folder...")
            os.mkdir(path)
            os.mkdir(os.path.join(path,"images"))
            file_path = os.path.join(path, "description.txt")
            w = csv.writer(open(file_path, "w"))
            for key, val in self.debug_conf.items():
                w.writerow([key, (str)(val)])

            self.path_to_log = os.path.join(path, "logs.csv")
            f = open(self.path_to_log, 'w')
            writer = csv.writer(f)
            self.headers = ["Epoch","Loss train","Loss val","Deviation train", "Deviation val"]
            writer.writerow(["Epoch","Loss train","Loss val","Deviation train", "Deviation val"])
            f.close()

        else:
            print("Logging is disabled... Please enable logging in config")
        return True

    def log(self, arr):
        f = open(self.path_to_log, 'a')
        writer = csv.writer(f)
        writer.writerow(arr)
        f.close()


    def create_report(self):
        df = pd.read_csv(self.path_to_log, names = self.headers )
        df = df.iloc[1: , :]

        df['Epoch']           = df['Epoch'].astype("float")
        df['Loss train']      = df['Loss train'].astype("float")
        df['Loss val']        = df['Loss val'].astype("float")
        df['Deviation train'] = df['Deviation train'].astype("float")
        df['Deviation val']   = df['Deviation val'].astype("float")
        plt.clf()
        df_loss = df[['Epoch','Loss train', 'Loss val']]
        ax = plt.gca()
        df_loss.plot(kind='line', x='Epoch', y='Loss train', color='steelblue', ax=ax)
        df_loss.plot(kind='line', x='Epoch', y='Loss val', color='orange', ax=ax)
        plt.savefig(os.path.join(self.path_folder,"loss.jpg" ))

        plt.clf()
        df_loss = df[['Epoch', 'Deviation train', 'Deviation val']]
        ax = plt.gca()
        df_loss.plot(kind='line', x='Epoch', y='Deviation train', color='steelblue', ax=ax)
        df_loss.plot(kind='line', x='Epoch', y='Deviation val', color='orange', ax=ax)
        plt.savefig(os.path.join(self.path_folder, "deviation.jpg"))