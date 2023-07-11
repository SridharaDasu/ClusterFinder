import numpy as np
from PIL import Image
from tqdm import tqdm

filePath = "./data/Raw_Data_Real.npy"
caltype = "ECAL"
dataPath, imgPath = "./data/RealDataImages/", "input/"+caltype+"_img_"

RAWDATA = np.load(filePath)

for idx, data in tqdm(enumerate(RAWDATA)):
    inputImg = np.transpose(data) # 30x25 ---> 25x30

    # converting data to image format
    inputImg = inputImg/np.max(inputImg)

    # padding to square
    inputImg = np.pad(inputImg, ((3, 4), (1, 1)), 'constant')
    inputImg = 1 - inputImg

    inputImg = np.array(inputImg * 255, dtype = np.uint8)

    inputImg = Image.fromarray(inputImg)
    inputImg.save(dataPath+imgPath+str(idx)+".png")