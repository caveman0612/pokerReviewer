import sys
import os

value = "save"

if (len(sys.argv) > 1):
    value = sys.argv[1]

string = f"{value}"
os.system("git add *")
os.system(f"git commit -m  {value}")
os.system("git push")