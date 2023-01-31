# $ source venv/Scripts/activate
from analyser.controller import Controller
from analyser.videoExtractor import VideoExtractor
from analyser.imageModifier import ImageModifier
from pathlib import Path
import os
# 57.5 frames per second


Video_FILE = "./video/test.mp4"

videoExtractor = VideoExtractor(Video_FILE)
imageModifier = videoExtractor.ImageModifier


parent_dir = Path(__file__).parent.absolute()
imageLoc = os.path.join(parent_dir, "images")

frame = videoExtractor.get_frame(12200)
frame = imageModifier.cropImage(frame, ["player_title", "holeCard_left", "card_number"])
videoExtractor.showImage(frame)
# 38600 change situation 
# 12200 not working???? 
# 29180
# controller.loopThroughFrames(5000, 40000)