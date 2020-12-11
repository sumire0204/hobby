# 1回の処理で0.5s分のバイナリデータを読み込む
# 「0.9を超えて、0.1s後に0.1以下に下がる」が2回あった場合、2回手拍子と判定する

import pyaudio
import wave
import numpy as np
import time

# 音データフォーマット
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8096
RECORD_SECONDS = 0.5

SLEEP_TIME = 1
THRESHOLD= 0.5 # 閾値

def clap_detector():
    '''
    Args:
        ndarray: バイナリデータを数値(int16)に変換し、正規化した配列
    Returns:
        bool: 
    '''
    CLAP_CNT = 0

    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = CHUNK
    )

    while True:
        data = stream.read(CHUNK, exception_on_overflow = False)
        x = np.frombuffer(data, dtype="int16") / 32768.0

        # 閾値以上の場合、0.5秒間の音データを取得
        if x.max() > THRESHOLD:

            all = []
            all.append(data)
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK, exception_on_overflow = False)
                all.append(data)

            data = b''.join(all)
            x = np.frombuffer(data, dtype="int16") / 32768.0

            cnt = len(x)//5 #0.1sあたりのデータ数

            # 0~0.4sまで
            i = 0
            while i <= len(x) - cnt -1:
                if x[i] > 0.5 and x[i+cnt] < 0.1:
                    CLAP_CNT += 1
                    i += cnt
                    continue
                i += 1
            return CLAP_CNT
        # stream.close()
        # p.terminate()