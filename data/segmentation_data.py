import numpy as np
from PIL import Image

filePath = "./data/EMData-20230220.npy.npy" #"./data/EMData-20230220.npy"
caltype = "ECAL"
dataPath, imgPath, annPath = "./data/images10/", "input/"+caltype+"_img_", "annotations/"+caltype+"_annm_"

RAWDATA = np.load(filePath)

for idx, data in enumerate(RAWDATA):
    inputImg, annMap =  data[0], data[1]

    # converting data to image format
    inputImg = inputImg/np.max(inputImg)

    # padding to square
    inputImg = np.pad(inputImg, ((3, 4), (1, 1)), 'constant')
    inputImg = 1 - inputImg
    annMap = np.pad(annMap, ((3, 4), (1, 1)), 'constant')
    annMap = 1 - annMap
    #annMap += 1

    inputImg = np.array(inputImg * 255, dtype = np.uint8)
    annMap = np.array(annMap * 255, dtype = np.uint8)

    inputImg, annMap = Image.fromarray(inputImg), Image.fromarray(annMap)
    inputImg.save(dataPath+imgPath+str(idx)+".png")
    annMap.save(dataPath+annPath+str(idx)+".png")
