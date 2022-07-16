import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import sys

def wav_read(path):
    wave, fs = sf.read(path) #音データと周波数を読み込む
    return wave, fs

if __name__ == "__main__":
    args = sys.argv
    wave, fs = wav_read(args[1])
    time = np.arange(0,len(wave))/fs
    print(len(wave))
    plt.plot(time, wave)
    plt.show()
    plt.close()