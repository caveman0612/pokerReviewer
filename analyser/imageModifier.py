import cv2
from pytesseract import pytesseract

class ImageModifier: 
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

        "card_number": [0, .5],
        "card_suit": [.5, 1],
    }
    
    def __init__(self, filePath) -> None:
        pytesseract.tesseract_cmd = filePath
        self.pytesseract = pytesseract

    def cropImage(self, frame, section):
        img = frame
        for crop in section:
            cropped = self.croppedDict[crop]
            if crop[0:4] == "card":
                print(img.shape)
                height, width, _ = img.shape
                img = img[int(cropped[0] * height): int(cropped[1] * height), 0: width]
            else:
                img = img[cropped[0]:cropped[0] + cropped[2], cropped[1]:cropped[1] + cropped[3]]
        return img

    def resizeImage(self, frame, dimension):
        return cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)

    def match_template(self, image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

