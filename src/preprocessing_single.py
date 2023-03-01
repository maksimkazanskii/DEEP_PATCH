import pysam
import numpy as np
import random
import os
import cv2
import math
import argparse

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
    "count"       : 100
}

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

def is_unique(position, folder):
    for item in os.listdir(folder):
        position_current = int(item.split(".")[0])
        if math.fabs(position_current-position)<WINDOW_SIZE:
            return False
    return True

def analyze_the_file(folder_in, folder_out, filename):
    sub_folder_name = filename.split("_")[0].split("/")[-1]

    sub_folder = os.path.join(folder_out, sub_folder_name)
    if (os.path.isdir(sub_folder)):
        pass
    else:
        print("Created folder ", sub_folder)
        os.mkdir(sub_folder)

    full_filename = os.path.join(folder_in, filename)
    samfile = pysam.AlignmentFile(full_filename, "rb")
    # print(samfile.get_index_statistics())
    # first_position = samfile.get_first_position()
    # last_position  = samfile.get_last_position()
    list_of_windows = []
    i = 0
    count=0
    seq_length = get_seq_length(samfile)
    while i <= seq_length and count <CONFIG['count']:
        position = random.randint(1,10e8)
        read_arr = []
        for read in samfile.fetch('1', position, position + WINDOW_SIZE + 1):
            if (is_covered(read.get_reference_positions(), np.arange(position, position + WINDOW_SIZE + 1))):
                read_arr.append(read)

        if (len(read_arr) >= KERNEL_SIZE):
            # Window sequence quality
            window_sqr = preprocess(read_arr, np.arange(position, position + WINDOW_SIZE + 1))
            window_sqr = window_sqr[:WINDOW_SIZE, :WINDOW_SIZE]
            print("Order Number", i, "Position", position, len(read_arr))
            filename_img = os.path.join(sub_folder,(str)(position)+".png")

            if is_unique(position, sub_folder, WINDOW_SIZE):
                 cv2.imwrite(filename_img, window_sqr)
                 count=count+1
        i += 1

WINDOW_SIZE = CONFIG['WINDOW_SIZE']
KERNEL_SIZE = CONFIG['KERNEL_SIZE']

parser = argparse.ArgumentParser()
folder_in  = parser.add_argument('folder_in', type=str)
folder_out = parser.add_argument('folder_out', type=str)

print(folder_in, folder_out)
#for filename in os.listdir(folder_in):
#    if filename.endswith("bam"):
#        analyze_the_file(folder_in, folder_out, filename)



# python preprocess.py folder