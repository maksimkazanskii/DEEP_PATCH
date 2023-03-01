import os
import pandas
import shutil
import csv
import cv2

target_images_folder = "../../images_clean"
target_csv    = "../../labels/labels.csv"

origin_csv = "../../labels/age_raw.csv"
origin_images_folder = "../../images"
LIMIT = 100

def clean_images():

    #
    # create and clean the folder images_clean
    #
    try:
        shutil.rmtree(target_images_folder)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    try:
        os.mkdir(target_images_folder)
    except OSError:
        print("Creation of the directory %s failed" % target_images_folder)
    else:
        print("Successfully created the directory %s" % target_images_folder)

    with open(target_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['bam_name', 'age'])

    #
    # Creating the filenames and ages dictionary
    #

    with open(origin_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bam_name = row['bam_name']
            folder_name = os.path.join(origin_images_folder, bam_name+".bam")
            if os.path.exists(folder_name):
                new_foldername = os.path.join(target_images_folder, bam_name)
                try:
                    os.mkdir(new_foldername)
                except OSError:
                    print("Creation of the directory %s failed" % target_images_folder)
                else:
                    print("Successfully created the directory %s" % target_images_folder)
                print("Analyzing images for {}".format(folder_name))
                count = 0
                for file in os.listdir(folder_name):
                    img = cv2.imread(os.path.join(folder_name,file))
                    img = img.reshape((20, 20, 3))
                    new_filepath = os.path.join(new_foldername, file)
                    print("Writing a file {}".format(new_filepath))
                    cv2.imwrite(new_filepath, img)
                    count+=1
                    with open(target_csv, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow([row['bam_name'], row['age']])
                    if count==100:
                        break

                if count<100:
                    try:
                        shutil.rmtree(new_foldername)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))

clean_images()