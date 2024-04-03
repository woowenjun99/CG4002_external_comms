from typing import List
from time import perf_counter
from scipy.stats import median_absolute_deviation, iqr
from pynq import Overlay, allocate
import numpy as np
import statistics
from utils.logger import Logger, INFO

class AILogic:
    def __init__(self):
        overlay = Overlay("/home/xilinx/external_comms/ai/design_1.bit")
        self.dma = overlay.axi_dma_0
        self.input_buffer = allocate(shape=(36,), dtype=np.float32)
        self.output_buffer = allocate(shape=(1,), dtype=np.float32)
    
    def process(self, message: List[List[float]]) -> str:
        ####################### Start of AI logic ########################
        ai_actions = ["ironMan", "hulk", "captAmerica", "shangChi", "bomb", "shield", "reload", "logout", "nothing"]
        sample = np.array(message)
        for m in sample:
            for n in m:
                if n >= 32768:
                    binary = bin(n)
                    binary = binary[2:]
                    inverted = ''.join('10'[int(x)] for x in binary)
                    n = int(inverted, 2)
                    n += 1
                    n *= -1
                n /= 1000.0
        X = []
        for dim in range(6):
            v = sample[:,dim]
            max = np.max(dim)
            for val in v:
                val = val / (max + 1e-12)
            sample[:,dim] = v
        for i in range(6):
            vals = sample[:,i]
            mean = statistics.mean(vals)
            mad = median_absolute_deviation(vals)
            std = statistics.stdev(vals)
            inqr = iqr(vals)
            max = np.max(vals)
            min = np.min(vals)
            col = [mean, mad, std, inqr, max, min]
            X.extend(col)

        for i, n in enumerate(X):
            self.input_buffer[i] = n
        self.dma.sendchannel.transfer(self.input_buffer)
        self.dma.recvchannel.transfer(self.output_buffer)
        self.dma.sendchannel.wait()
        self.dma.recvchannel.wait()

        result = ai_actions[int(self.output_buffer[0])]

        # result = ai_actions[randint(0, len(ai_actions) - 1)]
        ####################### End of AI logic ##########################
        return result