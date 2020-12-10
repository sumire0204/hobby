import pyaudio
import wave
import numpy as np
from datetime import datetime
import time
import hue_controller
import clap_detector

SLEEP_TIME = 0.1

if __name__ == '__main__':

    while True:
        CLAP_CNT = clap_detector.clap_detector()
        print(CLAP_CNT)
        if CLAP_CNT == 2:
            hue_controller.request2hue()
            continue
        time.sleep(SLEEP_TIME) # 連続して実行されないようにする