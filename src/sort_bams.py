import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--folder')
args = parser.parse_args()
folder_of_interest= args.folder
for file in os.listdir(folder_of_interest):
    if file.endswith(".bam"):
        print("Sorting bam file ", file)
        index_request = "samtools index " + os.path.join(folder_of_interest, file)
        print(index_request)
        subprocess.call(index_request, shell = True,stdout=subprocess.DEVNULL)
        sort_request = "samtools sort " +  os.path.join(folder_of_interest, file)
        print(sort_request)
        subprocess.call(sort_request, shell = True,stdout=subprocess.DEVNULL)
        
# python sort_bams.py  --folder "../../data"