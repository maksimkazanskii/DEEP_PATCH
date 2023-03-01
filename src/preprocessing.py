import pysam
import numpy as np
import random
import os
import cv2
import math
import argparse
import time
from datetime import date
from datetime import datetime

CONFIG ={
    "ENCODING":
        {
         "A": 0,
         "T":75,
         "C":150,
         "G":225,
         "c":150,
         "g":225,
         "a":0,
         "t":75
        },
    "WINDOW_SIZE" : 20,
    "KERNEL_SIZE" : 20,
    "count"       : 110
}
WINDOW_SIZE = CONFIG['WINDOW_SIZE']
KERNEL_SIZE = CONFIG['KERNEL_SIZE']

def seq_to_numeric(sequence):
    arr =[]
    for char in sequence:
        arr.append(CONFIG['ENCODING'][char])
    return arr

def is_covered(read_positions, interval):

    mask = np.isin(interval, read_positions)
    value =np.prod(mask)
    return value

def normalize_quality(quality_arr):
    quality_arr =np.clip(quality_arr, 35, 45)
    quality_arr = (quality_arr -34 )*25
    return quality_arr

def get_seq_length(samfile):
    #
    # TODO : return the length of the sequence using pysam
    #
    samfile2 = samfile
    return 10e7

def preprocess(read_arr, window):
    start = window[0]
    end = window[0]+len(window)-1
    positions_arr = []
    sequence_arr  = []
    quality_arr   = []
    reference_arr = []
    for read in read_arr:
        reference = read.get_reference_sequence()
        reference = seq_to_numeric(reference)
        sequence  = read.get_forward_sequence()
        sequence = seq_to_numeric(sequence)

        quality   = np.array(read.get_forward_qualities())
        positions = np.array(read.get_reference_positions())
        start_pos = np.where(positions == start)[0][0]
        end_pos   = np.where(positions == end)[0][0]

        quality_arr.append(quality[start_pos:end_pos])
        positions_arr.append(positions[start_pos:end_pos])
        sequence_arr.append(sequence[start_pos: end_pos])
        reference_arr.append(reference[start_pos:end_pos])

    quality_arr   = np.array(quality_arr)
    sequence_arr  = np.array(sequence_arr)
    reference_arr = np.array(reference_arr)
    quality_arr = normalize_quality(quality_arr)
    sqr = np.dstack((sequence_arr,quality_arr, reference_arr))
    print("position_shape:",sqr.shape)
    return sqr

def is_unique(position, folder,WINDOW_SIZE):
    for item in os.listdir(folder):
        position_current = int(item.split(".")[0])
        if math.fabs(position_current-position)<WINDOW_SIZE:
            return False
    return True

class logger:

  def __init__(self, name):
    self.filename = "../logger/" + name + ".txt"
    with open(self.filename, "w") as f:
        f.write(" ")

  def write_log(self, string):
      with open(self.filename, "a") as f:
          f.write(string +"\n")

def analyze_the_file(folder_in, folder_out, filename, logger):
    sub_folder_name = filename.split("_")[0].split("/")[-1]
    sub_folder = os.path.join(folder_out, sub_folder_name)
    if os.path.isdir(sub_folder):
        print(" Filename was analyzed before... skipped")
        logger.write_log(" Filename was analyzed before... skipped")
        return False
    else:
        stry = "Created folder " +  sub_folder
        logger.write_log(stry)
        os.mkdir(sub_folder)
    try:
        full_filename = os.path.join(folder_in, filename)
        samfile = pysam.AlignmentFile(full_filename, "rb")
        i = 0
        count=0
        seq_length = get_seq_length(samfile)
    except:
        print("EXCEPTION: impossible to analyze a file")
        logger.write_log("EXCEPTION: impossible to analyze a file")
        return True
    exception_count=0
    while i <= seq_length and count <CONFIG['count']:
        try:
            position = random.randint(1,10e8)
            read_arr = []
            for read in samfile.fetch('1', position, position + WINDOW_SIZE + 1):
                if is_covered(read.get_reference_positions(), np.arange(position, position + WINDOW_SIZE + 1)):
                    read_arr.append(read)
            if (len(read_arr) >= KERNEL_SIZE):
                window_sqr = preprocess(read_arr, np.arange(position, position + WINDOW_SIZE + 1))
                window_sqr = window_sqr[:WINDOW_SIZE, :WINDOW_SIZE]
                stry = "Order Number "+ str(i) + " Position " + str(position) + str(len(read_arr))
                print(stry)
                logger.write_log(stry)
                filename_img = os.path.join(sub_folder,str(position)+".png")
                if is_unique(position, sub_folder, WINDOW_SIZE):
                    cv2.imwrite(filename_img, window_sqr)
                    count=count+1
        except Exception as e:
            exception_count+=1
            print("EXCEPTION: The error in the BAM (additional symbols)")

        if exception_count>100:
            logger.write_log("EXCEPTION: multiple errors in the BAM file (additional symbols)")
            return True
        i += 1
    return True

parser = argparse.ArgumentParser()
parser.add_argument('--folder_in')
parser.add_argument('--folder_out')
args = parser.parse_args()
folder_in  = args.folder_in
folder_out = args.folder_out
print("\nfolder_in: ",folder_in,  " folder_out: ",folder_out," \n\n")

today = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
logger = logger(str(today) +str(" ")+ str(current_time))
for filename in os.listdir(folder_in):
    if filename.endswith("bam"):
        print("****************************")
        print("ANALYZING filename", filename)
        result = analyze_the_file(folder_in, folder_out, filename, logger)
        if not result:
            pass
        if result:
            print(" Filename  is analyzed successfully")
