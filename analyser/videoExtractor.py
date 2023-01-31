import cv2
# import numpy as np
# import matplotlib.pyplot as plt
import os
# from pathlib import Path
from pytesseract import pytesseract
# import shutil
from analyser.imageModifier import ImageModifier
from analyser.methods import Decorators

class VideoExtractor:

    def __init__(self, video_file) -> None:
        self.video_file = video_file
        self.video=cv2.VideoCapture(self.video_file)
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        self.newFileName = os.path.join("C:\Program Files\Tesseract-OCR", f"tesseract.exe")
        pytesseract.tesseract_cmd = self.newFileName
        self.pytesseract = pytesseract

        self.ImageModifier = ImageModifier(self.newFileName)

    def get_frame(self, fNum):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, fNum)
            _, image = self.video.read()
            return image

    # @Decorators.get_grayscale
    def showImage(self, image):
        cv2.imshow("Output", image)
        cv2.waitKey(0)
    
    def saveImage(self, frame, location, name):
        cv2.imwrite(location + f"\{name}.jpg", frame)