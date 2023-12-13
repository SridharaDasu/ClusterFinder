import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

def generate_border(image, border_size=1, n_erosions=1):

    erosion_kernel = np.ones((1,1), np.uint8)      ## Start by eroding edge pixels
    eroded_image = cv2.erode(image, erosion_kernel, iterations=n_erosions)  
 
    ## Define the kernel size for dilation based on the desired border size (Add 1 to keep it odd)
    kernel_size = 2*border_size + 1 
    dilation_kernel = np.ones((kernel_size, kernel_size), np.uint8)   #Kernel to be used for dilation
    dilated  = cv2.dilate(eroded_image, dilation_kernel, iterations = 1)
    
    ## Replace 255 values to 127 for all pixels. Eventually we will only define border pixels with this value
    dilated_127 = np.where(dilated == 255, 3, dilated)
    original_with_border = np.where(eroded_image > 127, 1, dilated_127)
    original_with_border = np.where(original_with_border == 0, 2, original_with_border)
    
    return original_with_border
 

from pathlib import Path
cal_type = "ECAL"
data_path, ann_path = "./data/", "annotations/"+cal_type+"_annm_*.*"
out_path = "trimaps/"

for file in glob.glob(data_path+ann_path):
    name = Path(file).stem  #Extract name so processed images can be saved under the same name
    img= cv2.imread(file, cv2.IMREAD_GRAYSCALE)  #now, we can read each file since we have the full path    
    #process each image
    processed_image = generate_border(img, border_size=1, n_erosions=1)
    #Save images with same name as original image/mask
    cv2.imwrite(data_path+ out_path + name + ".png", processed_image)
    print("Finished processing image ", name)