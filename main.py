import pyaudio
import wave
import numpy as np
from datetime import datetime
import time
import hue_controller

# 音データフォーマット
CHUNK = 1024
CHUNK = CHUNK*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.5

SLEEP_TIME = 1.0/100
THRESHOLD= 0.5 # 閾値

if __name__ == '__main__':

    # 音の取込開始
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = CHUNK
    )

    while stream.is_active():
        # バイナリデータを取得し、ndarrayに変換、正規化
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0

        # 閾値以上の場合はhueのAPIを叩く
        if x.max() > THRESHOLD:
            hue_controller.request2hue()
            time.sleep(SLEEP_TIME) # 連続して実行されないようにする

    # stream.close()
    # p.terminate()

start = time.time()
    for i in range(0,11):
        print "a"
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")