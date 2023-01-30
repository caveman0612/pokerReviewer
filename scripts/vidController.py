import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from pytesseract import pytesseract
import shutil
from scripts.imageMod import ImageMod



class VidController:
    # croppedDict = {
    #     "player_title": [497, 151, 100, 100],
    #     "holeCard_left": [8, 16, 43, 33],
    #     "holeCard_right": [8, 48, 43, 33],

    #     "flopCard_left": [277, 74, 70, 50],
    #     "flopCard_middle": [277, 124, 70, 50],
    #     "flopCard_right": [277, 174, 70, 50],
    #     "turnCard": [277, 223, 70, 50],
    #     "RiverCard": [277, 273, 70, 50],

    #     "left_bottom": [361, 18, 100, 100],
    #     "left_top": [155, 18, 100, 100],
    #     "top_top": [65, 150, 100, 100],
    #     "right_top": [155, 277, 100, 100],
    #     "right_bottom": [361, 277, 100, 100],

    #     "get_player_stack": [50, 25, 20, 60],
    #     "get_player_number": [50, 5, 20, 20],
    #     "get_player_left_card": [18, 23, 35, 28],
    #     "get_player_right_card": [18, 48, 35, 28],

    #     "final_display": [50, 235, 80, 130],

    #     "card_suit": [],
    #     "card_number": [],
    # }



    def __init__(self, video_file) -> None:
        self.video_file = video_file
        self.video=cv2.VideoCapture(self.video_file)
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        self.newFileName = os.path.join("C:\Program Files\Tesseract-OCR", f"tesseract.exe")
        pytesseract.tesseract_cmd = self.newFileName
        self.pytesseract = pytesseract

        self.ImageMod = ImageMod(self.newFileName)
        

    def getHoleCards(self, image, getImage):
        holeCard = []
        sections = ["holeCard_left", "holeCard_right"]
        for areas in sections:
            card = []
            number = self.ImageMod.cropImage(image, ["player_title", areas, "card_number"])
            number = self.ImageMod.get_grayscale(number)
            if getImage == False:
                number = self.ImageMod.getNumberFromImage(number)
            suit = self.ImageMod.cropImage(image, ["player_title", areas, "card_suit"])
            suit = self.ImageMod.get_grayscale(suit)
            if getImage == False:
                suit = self.ImageMod.getSuitFromImage(suit)
            card.append(number)
            card.append(suit)
            holeCard.append(card)
        return holeCard

    def getEveryonesStachSize(self, image):
        sections = ["player_title", "left_bottom","left_top","top_top","right_top","right_bottom"]
        stacks = []
        for section in sections:
            player = {}
            stack = self.ImageMod.cropImage(image, [section, "get_player_stack"])
            stack = self.ImageMod.imgCoversionForStacks(image)

            number = self.ImageMod.cropImage(image, [section, "get_player_number"])
            number = self.ImageMod.imgConversionForNumbers(image)

            player["stack"] = stack
            player["number"] = number
            # print(player["number"])
            stacks.append(player)
        return stacks


    def getTableCardImgNumber(self, image):
        holeCard = []
        sections = ["flopCard_left", "flopCard_middle", "flopCard_right", "turnCard", "RiverCard"]
        for areas in sections:
            cropped = self.ImageMod.cropImage(image, [areas,"tableCard_number"])
            cropped = self.ImageMod.get_grayscale(cropped)
            holeCard.append(cropped)
        return holeCard

    def get_frame(self, fNum):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, fNum)
            _, image = self.video.read()
            return image

    def loopThroughFrames(self, start, stop):
        self.deleteDirectory("./images")
        parent_dir = Path(__file__).parent.parent.absolute()
        sample_rate = 1000
        prev1 = [[]]
        for fNum in range(start, stop , sample_rate):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, fNum)
            _, image = self.video.read()
            newFileName = os.path.join(parent_dir, f"images\{fNum}")
            
            self.getAllStackSizesAndSave(image, newFileName)
            # prev1 = self.getAllWholeCardsAndSave(image, prev1, newFileName)

    def getAllStackSizesAndSave(self, image, newFileName):
        stacks = self.getEveryonesStachSize(image)
        if not os.path.exists(newFileName):
                os.makedirs(newFileName)
        for stack in stacks:
            # print(stack)
            num = stack.get("number")
            numStr = self.ImageMod.getNumberFromImage(num, "--psm 13")
            money = stack.get("stack")
            moneyStr = self.ImageMod.getNumberFromImage(money, "--psm 13")
            
            self.ImageMod.saveImage(num, newFileName, f"{numStr}_num")
            self.ImageMod.saveImage(money, newFileName, f"{moneyStr}_num")
    
    def getAllWholeCardsAndSave(self, image, prev1, newFileName):
        arr = self.getHoleCards(image, True)
        cards = []
        cardsImage = []
        for card in arr:
            num, suit = card
            numStr = self.ImageMod.imgCovertsionForCards(num)
            # num = self.applyAddaptiveThresholdingMean(num)
            # num = self.applyThresholdingOtsu(num)
            
            # numStr = self.getNumberFromImage(num)
            if (numStr):
                cards.append(numStr)
                cardsImage.append([num, suit])
        
        if (cards[0] in prev1[len(prev1) - 1] and cards[1] in prev1[len(prev1) - 1]) or (cards[0] in prev1[len(prev1) - 2] and cards[1] in prev1[len(prev1) - 2]):
            pass
        else:
            pass
            if not os.path.exists(newFileName):
                os.makedirs(newFileName)
            self.ImageMod.saveImage(cardsImage[0][0], newFileName, f"{cards[0]}_num")
            self.ImageMod.saveImage(cardsImage[0][1], newFileName, f"{cards[0]}_suit")
            self.ImageMod.saveImage(cardsImage[1][0], newFileName, f"{cards[1]}_num")
            self.ImageMod.saveImage(cardsImage[1][1], newFileName, f"{cards[1]}_suit")
            prev1.append(cards)
        return prev1        
            

    # def getAllCards(self, frame, fNum):
    #     holeArray = self.getHoleCardImgNumber(frame)
    #     tableArray = self.getTableCardImgNumber(frame)
    #     holeNumbers = self.getNumberFromImage(holeArray)
    #     tableNumbers = self.getNumberFromImage(tableArray)
    #     # print(fNum, holeNumbers, tableNumbers)


    def deleteDirectory(self, folder):
        # dir_path = '/images'
        try:
            shutil.rmtree(folder)
        except OSError as e:
            print("Error: %s : %s" % (folder, e.strerror))

        os.makedirs("./images")
