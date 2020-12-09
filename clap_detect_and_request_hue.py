import pyaudio
import wave
import numpy as np
from datetime import datetime
import subprocess

# 音データフォーマット
# chunk = 1024
chunk = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.5

# 閾値
threshold = 0.2

# 音の取込開始
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

cnt = 0

while True:
    # 音データの取得
    data = stream.read(chunk)
    # ndarrayに変換
    x = np.frombuffer(data, dtype="int16") / 32768.0

    # 閾値以上の場合はファイルに保存
    if x.max() > threshold:
        # import request_hue_api
        cmd = "Python request_hue_api.py"
        subprocess.call(cmd.split())
    
        cnt += 1

    # 5回検出したら終了
    if cnt > 5:
        break

stream.close()
p.terminate()

# print("!!")
# import test
# print("world")