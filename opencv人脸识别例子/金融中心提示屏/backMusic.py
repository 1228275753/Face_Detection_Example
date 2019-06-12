import sys
from playsound import playsound
while True:
    sound = playsound(sys.argv[1])
    print("音频名字为:",sound)