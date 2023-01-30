# $ source venv/Scripts/activate
from scripts.vidController import VidController
from pathlib import Path
import os
# 57.5 frames per second


Video_FILE = "./video/test.mp4"

controller = VidController(Video_FILE)


parent_dir = Path(__file__).parent.absolute()
imageLoc = os.path.join(parent_dir, "images")

# frame = controller.get_frame(12200)
# controller.showImage(frame)
# 38600 change situation 
# 12200 not working???? 
# 29180
controller.loopThroughFrames(5000, 40000)









