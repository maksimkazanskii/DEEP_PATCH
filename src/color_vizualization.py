import os
import cv2
import numpy as np
folder     = "../output/I2367"
folder_out = "../output/color_visualization/"
full_image= np.array([])
print(os.getcwd())
REVERSE_ENCODING={
         0 :"A",
         75: "T",
         150: "C",
         225: "G"}

for item in os.listdir(folder):
    img = cv2.imread(os.path.join(folder,item))
    if (len(full_image)==0):
        full_image = img
    else:
        full_image =np.concatenate((full_image,img))

color_dict   = {}
scheme_dict  = {}
for i in range(len(full_image)):
    for j in range(len(full_image[0])):
        if (str)(full_image[i][j]) in color_dict.keys():
            color_dict[(str)(full_image[i][j])]+=1
        else:
            color_dict[(str)(full_image[i][j])]=0
            scheme_dict[(str)(full_image[i][j])] = full_image[i][j]
print(color_dict)
for key, value in sorted(color_dict.items()): # Note the () after items!
    a     = np.array([50, 50])
    arr   = scheme_dict[key]
    image = np.tile(arr,(50,50))
    image= image.reshape((50,50,3))
    name  = "NUMBER: " + (str)(color_dict[key]) +  " SEQ: " + (str)(REVERSE_ENCODING[arr[0]])+" |  REF: "+str(REVERSE_ENCODING[arr[2]]) + " | QUAL: " +(str)(arr[1])
    print(name)
    cv2.imwrite(os.path.join(folder_out,name+".png"), image)