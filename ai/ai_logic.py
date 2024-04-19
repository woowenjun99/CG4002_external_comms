from typing import List
from pynq import Overlay, allocate
import numpy as np
import statistics
# from scipy.stats import median_absolute_deviation, iqr, skew, kurtosis

class AILogic:
    def __init__(self):
        overlay = Overlay("/home/xilinx/external_comms/ai/design_1.bit")
        self.dma = overlay.axi_dma_0
        self.input_buffer = allocate(shape=(48,), dtype=np.float32)
        self.output_buffer = allocate(shape=(1,), dtype=np.float32)
    
    def process(self, message: List[float]) -> str:
        ####################### Start of AI logic ########################
        ai_actions = ["ironMan", "hulk", "captAmerica", "shangChi", "bomb", "shield", "reload", "logout", "nothing"]
        sample = message

        # transform it from 180 to 30 rows of 6 columns
        final = [sample[i:i + 6] for i in range(0, len(sample), 6)]
        sample = np.array(final, dtype=np.float64)

        X = []
        sample = final / final.max(axis=0)
        print(f"SAMPLE: {sample}")

        # Scaling the data
        for i in range(6):
            # vals = sample[:,i]
            # mean = statistics.mean(vals)
            # mad = median_absolute_deviation(vals)
            # std = statistics.stdev(vals)
            # inqr = iqr(vals)
            # max = np.max(vals)
            # min = np.min(vals)
            # skewness = skew(vals)
            # kurt = kurtosis(vals)
            # col = [mean, mad, std, inqr, max, min, skewness, kurt]
            col = [0, 0, 0, 0, 0, 0, 0, 0]
            X.extend(col)

        for i, n in enumerate(X):
            self.input_buffer[i] = n

        try:
            self.dma.sendchannel.transfer(self.input_buffer)
            self.dma.recvchannel.transfer(self.output_buffer)
            self.dma.sendchannel.wait()
            self.dma.recvchannel.wait()
            result = ai_actions[int(self.output_buffer[0])]
        except Exception as e:
            print(f"ERROR is {e}")
            result = ai_actions[-1]
        print(f"THE RESULT IS {result}")

        ####################### End of AI logic ##########################
        return result