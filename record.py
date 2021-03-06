import pyaudio
import wave
import numpy as np
from datetime import datetime

# 音データフォーマット
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
# RATE = 44100
RATE = 4410
RECORD_SECONDS = 0.5

# 閾値
threshold = 0.8

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
    data = stream.read(chunk exception_on_overflow = False)
    # ndarrayに変換
    x = np.frombuffer(data, dtype="int16") / 32768.0

    # 閾値以上の場合はファイルに保存
    if x.max() > threshold:
        filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".wav"
        print(cnt, filename)

        # 2秒間の音データを取込
        all = []
        all.append(data)
        for i in range(0, int(RATE / chunk * int(RECORD_SECONDS))):
            data = stream.read(chunk, exception_on_overflow = False)
            all.append(data)
        data = b''.join(all)

        # 音声ファイルとして出力
        out = wave.open(filename,'w')
        out.setnchannels(CHANNELS)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(data)
        out.close()

        print("Saved.")

stream.close()
p.terminate()