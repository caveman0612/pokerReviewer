import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from pytesseract import pytesseract
import shutil
# from imageMod import ImageMod

class ImageMod:
    croppedDict = {
        # "holeCard": [509, 170, 36, 59], 
        "player_title": [497, 151, 100, 100],
        "holeCard_left": [8, 16, 43, 33],
        "holeCard_right": [8, 48, 43, 33],
        # "holeCard_suit": [18, 5, 18, 24],
        # "HoleCard_number":[0, 0, 18, 24],

        "flopCard_left": [277, 74, 70, 50],
        "flopCard_middle": [277, 124, 70, 50],
        "flopCard_right": [277, 174, 70, 50],
        "turnCard": [277, 223, 70, 50],
        "RiverCard": [277, 273, 70, 50],
        # "tableCard_suit": [35, 30, 18, 24],
        # "tableCard_number":[5, 5, 25, 30],

        "left_bottom": [361, 18, 100, 100],
        "left_top": [155, 18, 100, 100],
        "top_top": [65, 150, 100, 100],
        "right_top": [155, 277, 100, 100],
        "right_bottom": [361, 277, 100, 100],

        "get_player_stack": [50, 25, 20, 60],
        "get_player_number": [50, 5, 20, 20],
        "get_player_left_card": [18, 23, 35, 28],
        "get_player_right_card": [18, 48, 35, 28],

        "final_display": [50, 235, 80, 130],

        "card_suit": [],
        "card_number": [],
    }

    def __init__(self, filePath) -> None:
        pytesseract.tesseract_cmd = filePath
        self.pytesseract = pytesseract

    # def imageToData(self, frame):
    #     return self.pytesseract.image_to_data(frame)
        
    def saveImage(self, frame, location, name):
        cv2.imwrite(location + f"\{name}.jpg", frame)
        return True

    def cropImage(self, frame, section):
        img = frame
        for crop in section:
            if crop[0:4] == "card":
                height, width, _ = img.shape
                if crop[5] == "s":
                    img = img[int(height * 0.5):height , 0: width]
                if crop[5] == "n":
                    img = img[0: int(height * 0.5), 0: width]
            else:
                cropped = self.croppedDict[crop]
                img = img[cropped[0]:cropped[0] + cropped[2], cropped[1]:cropped[1] + cropped[3]]
        return img

    def resizeImage(self, frame, dimension):
        return cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)

    def getSuitFromImage(self, imgs):
        return "_"

    def getNumberFromImage(self, imgs, config):
        print(imgs.shape, config)
        text = pytesseract.image_to_string(imgs, config=config)
        if text:
            text = text[0]
            return text


    def imgCovertsionForCards(self, image):
        image = self.get_grayscale(image)
        image = self.applyAddaptiveThresholdingMean(image)
        image = self.applyThresholdingOtsu(image)
        numStr = self.getNumberFromImage(image, "--psm 13")
        return {"string": numStr, "image":image}
    
    def imgCoversionForStacks(self, image):
        image = self.get_grayscale(image)
        image = self.applyAddaptiveThresholdingMean(image)
        image = self.applyThresholdingOtsu(image)
        numStr = self.getNumberFromImage(image, "--psm 13")
        return {"string": numStr, "image":image}

    def imgConversionForNumbers(self, image):
        image = self.get_grayscale(image)
        image = self.applyAddaptiveThresholdingMean(image)
        image = self.applyThresholdingOtsu(image)
        numStr = self.getNumberFromImage(image, "--psm 13")
        return {"string": numStr, "image":image}

    def imgConversionForSuits(self, image):
        pass


    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(self, image):
        return cv2.medianBlur(image,5)
    
    #thresholding
    # def thresholding(self, image):
    #     return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #dilation
    def dilate(self, image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)
        
    #erosion
    def erode(self, image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(self, image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    #skew correction
    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def gaussianBlur(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    #template matching
    def match_template(self, image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

    def applyAddaptiveThresholdingMean(self, image):
        return cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)

    def applyAddaptiveThresholdingGaussian(self, image):
        return cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    # def applyThresholding(self, image):
    #     blurred = cv2.GaussianBlur(image, (7, 7), 0)
    #     (T, threshInv) = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
    #     return threshInv

    def applyThresholding(self, image):
        (T, threshInv) = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY_INV)
        return threshInv

    def applyThresholdingOtsu(self, image):
        (T, threshInv) = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return threshInv

    def showImage(self, image):
        cv2.imshow("Output", image)
        cv2.waitKey(0)